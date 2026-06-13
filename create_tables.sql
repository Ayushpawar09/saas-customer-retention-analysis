-- ============================================================
-- StreamLine Analytics Database Schema
-- 8 tables for SaaS Customer Retention Analysis
-- ============================================================

DROP TABLE IF EXISTS cancellations CASCADE;
DROP TABLE IF EXISTS invoices CASCADE;
DROP TABLE IF EXISTS support_tickets CASCADE;
DROP TABLE IF EXISTS product_usage CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS subscriptions CASCADE;
DROP TABLE IF EXISTS plans CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
    customer_id          VARCHAR(20)   PRIMARY KEY,
    company_name         VARCHAR(150)  NOT NULL,
    industry             VARCHAR(80),
    company_size         VARCHAR(30),
    country              VARCHAR(60),
    city                 VARCHAR(60),
    signup_date          DATE          NOT NULL,
    acquisition_source   VARCHAR(80),
    account_manager      VARCHAR(100),
    customer_segment     VARCHAR(30),
    first_name           VARCHAR(80),
    last_name            VARCHAR(80),
    email                VARCHAR(150)  UNIQUE NOT NULL,
    phone                VARCHAR(30),
    is_active            BOOLEAN       DEFAULT TRUE,
    created_at           TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE plans (
    plan_id              VARCHAR(20)   PRIMARY KEY,
    plan_name            VARCHAR(80)   NOT NULL,
    plan_tier            VARCHAR(30)   NOT NULL,
    billing_cycle        VARCHAR(20)   NOT NULL,
    monthly_price        DECIMAL(10,2) NOT NULL,
    annual_price         DECIMAL(10,2),
    max_users            INT,
    max_projects         INT,
    storage_gb           INT,
    has_api_access       BOOLEAN       DEFAULT FALSE,
    has_priority_support BOOLEAN       DEFAULT FALSE,
    has_custom_reports   BOOLEAN       DEFAULT FALSE,
    is_active            BOOLEAN       DEFAULT TRUE,
    created_at           TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subscriptions (
    subscription_id        VARCHAR(20)   PRIMARY KEY,
    customer_id            VARCHAR(20)   NOT NULL REFERENCES customers(customer_id),
    plan_id                VARCHAR(20)   NOT NULL REFERENCES plans(plan_id),
    status                 VARCHAR(30)   NOT NULL DEFAULT 'Active',
    start_date             DATE          NOT NULL,
    end_date               DATE,
    trial_end_date         DATE,
    cancelled_date         DATE,
    renewal_date           DATE,
    auto_renew             BOOLEAN       DEFAULT TRUE,
    discount_percent       DECIMAL(5,2)  DEFAULT 0.00,
    mrr_value              DECIMAL(10,2),
    previous_plan_id       VARCHAR(20)   REFERENCES plans(plan_id),
    upgrade_downgrade_flag VARCHAR(20),
    created_at             TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
    payment_id             VARCHAR(20)   PRIMARY KEY,
    customer_id            VARCHAR(20)   NOT NULL REFERENCES customers(customer_id),
    subscription_id        VARCHAR(20)   NOT NULL REFERENCES subscriptions(subscription_id),
    invoice_id             VARCHAR(20),
    payment_date           DATE,
    amount                 DECIMAL(10,2) NOT NULL,
    currency               VARCHAR(10)   DEFAULT 'USD',
    payment_method         VARCHAR(50),
    payment_status         VARCHAR(30)   NOT NULL,
    failure_reason         VARCHAR(150),
    retry_attempt          INT           DEFAULT 0,
    gateway_response       VARCHAR(100),
    is_recurring           BOOLEAN       DEFAULT TRUE,
    payment_period_start   DATE,
    payment_period_end     DATE,
    created_at             TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_usage (
    usage_id                    VARCHAR(20)   PRIMARY KEY,
    customer_id                 VARCHAR(20)   NOT NULL REFERENCES customers(customer_id),
    subscription_id             VARCHAR(20)   NOT NULL REFERENCES subscriptions(subscription_id),
    usage_date                  DATE          NOT NULL,
    active_users                INT           DEFAULT 0,
    total_sessions              INT           DEFAULT 0,
    avg_session_duration_mins   DECIMAL(8,2),
    projects_created            INT           DEFAULT 0,
    reports_generated           INT           DEFAULT 0,
    api_calls                   INT           DEFAULT 0,
    features_used               INT           DEFAULT 0,
    storage_used_gb             DECIMAL(8,2),
    login_count                 INT           DEFAULT 0,
    last_login_date             DATE,
    created_at                  TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE support_tickets (
    ticket_id              VARCHAR(20)   PRIMARY KEY,
    customer_id            VARCHAR(20)   NOT NULL REFERENCES customers(customer_id),
    subscription_id        VARCHAR(20)   REFERENCES subscriptions(subscription_id),
    ticket_date            DATE          NOT NULL,
    category               VARCHAR(80),
    priority               VARCHAR(20),
    status                 VARCHAR(30),
    subject                VARCHAR(200),
    channel                VARCHAR(40),
    assigned_agent         VARCHAR(100),
    resolution_date        DATE,
    resolution_time_hours  DECIMAL(8,2),
    csat_score             INT,
    is_escalated           BOOLEAN       DEFAULT FALSE,
    created_at             TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cancellations (
    cancellation_id              VARCHAR(20)  PRIMARY KEY,
    customer_id                  VARCHAR(20)  NOT NULL REFERENCES customers(customer_id),
    subscription_id              VARCHAR(20)  NOT NULL REFERENCES subscriptions(subscription_id),
    cancellation_date            DATE         NOT NULL,
    effective_date               DATE         NOT NULL,
    cancellation_reason_category VARCHAR(80),
    cancellation_reason_detail   VARCHAR(500),
    cancellation_type            VARCHAR(30),
    was_offered_discount         BOOLEAN      DEFAULT FALSE,
    discount_accepted            BOOLEAN      DEFAULT FALSE,
    competitor_name              VARCHAR(100),
    win_back_eligible            BOOLEAN      DEFAULT TRUE,
    feedback_score               INT,
    processed_by                 VARCHAR(100),
    created_at                   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invoices (
    invoice_id             VARCHAR(20)   PRIMARY KEY,
    customer_id            VARCHAR(20)   NOT NULL REFERENCES customers(customer_id),
    subscription_id        VARCHAR(20)   NOT NULL REFERENCES subscriptions(subscription_id),
    invoice_date           DATE          NOT NULL,
    due_date               DATE          NOT NULL,
    billing_period_start   DATE,
    billing_period_end     DATE,
    subtotal               DECIMAL(10,2) NOT NULL,
    discount_amount        DECIMAL(10,2) DEFAULT 0.00,
    tax_amount             DECIMAL(10,2) DEFAULT 0.00,
    total_amount           DECIMAL(10,2) NOT NULL,
    amount_paid            DECIMAL(10,2) DEFAULT 0.00,
    outstanding_amount     DECIMAL(10,2),
    invoice_status         VARCHAR(30),
    payment_terms          VARCHAR(30),
    days_overdue           INT           DEFAULT 0,
    created_at             TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);