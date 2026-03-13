-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- PRODUCTS KNOWLEDGE BASE (for bot)
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_hash TEXT UNIQUE NOT NULL,
    brand TEXT NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    price DECIMAL(10,2) NOT NULL,
    original_price DECIMAL(10,2),
    discount_percent INT,
    rating DECIMAL(2,1),
    review_count INT,
    description TEXT,
    tags TEXT[],
    image_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- LEADS TABLE
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_hash TEXT UNIQUE NOT NULL,
    
    -- Contact info
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    source TEXT CHECK (source IN ('telegram_user', 'whatsapp_user', 'website_form', 'instagram')),
    
    -- Conversation context
    conversation_history JSONB,
    preferred_categories TEXT[],
    interested_products UUID[],
    
    -- Enrichment
    company TEXT,
    role TEXT,
    industry TEXT,
    company_size INT,
    
    -- Aura-specific metrics
    purchase_intent INT CHECK (purchase_intent BETWEEN 0 AND 40),
    lot_size INT,                    -- How many units they might buy
    est_profit DECIMAL(10,2),         -- Estimated profit if converted
    customer_value_score INT CHECK (customer_value_score BETWEEN 0 AND 30),
    
    -- Final score (0-100)
    score INT CHECK (score BETWEEN 0 AND 100),
    score_breakdown JSONB,            -- Store component scores
    icp_fit TEXT CHECK (icp_fit IN ('high','medium','low')),
    
    -- State machine
    status TEXT NOT NULL DEFAULT 'queued'
        CHECK (status IN (
            'queued', 'scoring', 'pending_approval',
            'approved', 'rejected', 'snoozed',
            'in_sequence', 'converted', 'dead'
        )),
    sequence_started BOOLEAN DEFAULT FALSE,
    sequence_step INT DEFAULT 0,
    last_contacted TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- STATE TRANSITIONS
CREATE TABLE state_transitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    from_state TEXT,
    to_state TEXT,
    actor TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- CONVERSATION LOGS
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    platform TEXT CHECK (platform IN ('telegram', 'whatsapp', 'email')),
    direction TEXT CHECK (direction IN ('incoming', 'outgoing')),
    message TEXT,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ATOMIC STATE TRANSITION FUNCTION
CREATE OR REPLACE FUNCTION transition_lead(
    p_lead_id UUID,
    p_new_status TEXT,
    p_actor TEXT
) RETURNS BOOLEAN AS $$
DECLARE
    current_status TEXT;
    allowed BOOLEAN := FALSE;
BEGIN
    SELECT status INTO current_status FROM leads
    WHERE id = p_lead_id FOR UPDATE;

    -- Valid transitions
    IF (current_status = 'queued' AND p_new_status = 'scoring') OR
       (current_status = 'scoring' AND p_new_status = 'pending_approval') OR
       (current_status = 'pending_approval' AND p_new_status IN ('approved','rejected','snoozed')) OR
       (current_status = 'approved' AND p_new_status = 'in_sequence') OR
       (current_status = 'in_sequence' AND p_new_status IN ('converted','dead'))
    THEN allowed := TRUE; END IF;

    IF NOT allowed THEN RETURN FALSE; END IF;

    UPDATE leads SET status = p_new_status,
        updated_at = NOW() WHERE id = p_lead_id;
    INSERT INTO state_transitions VALUES (
        uuid_generate_v4(), p_lead_id, current_status,
        p_new_status, p_actor, NULL, NOW()
    );
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- START SEQUENCE FUNCTION (atomic)
CREATE OR REPLACE FUNCTION start_sequence_if_not_started(
    p_lead_id UUID
) RETURNS UUID AS $$
DECLARE
    updated_id UUID;
BEGIN
    UPDATE leads
    SET sequence_started = TRUE, 
        sequence_step = 1,
        status = 'in_sequence',
        updated_at = NOW()
    WHERE id = p_lead_id
      AND sequence_started = FALSE
      AND status = 'approved'
    RETURNING id INTO updated_id;
    
    RETURN updated_id;
END;
$$ LANGUAGE plpgsql;
