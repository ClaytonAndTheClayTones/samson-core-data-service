create table if not exists retailers (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
	name varchar(255) NOT NULL, 
    hq_city  varchar(255) NULL,
    hq_state varchar(255) NULL,
    hq_country varchar(2),
    account_status varchar(32) NOT NULL DEFAULT 'Unregistered',
    contact_email varchar(320) NULL, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   

CREATE INDEX IF NOT EXISTS idx_retailers_name ON public.retailers(name);  
CREATE INDEX IF NOT EXISTS idx_retailers_account_status ON public.retailers(account_status);  
CREATE INDEX IF NOT EXISTS idx_retailers_hq_city ON public.retailers(hq_city); 
CREATE INDEX IF NOT EXISTS idx_retailers_hq_state ON public.retailers(hq_state); 
CREATE INDEX IF NOT EXISTS idx_retailers_hq_country ON public.retailers(hq_country); 
CREATE INDEX IF NOT EXISTS idx_retailers_created_at ON public.retailers(created_at); 

-- Enums

ALTER TABLE public.retailers DROP CONSTRAINT IF EXISTS enum_retailers_account_status;
  
ALTER TABLE public.retailers  
   ADD CONSTRAINT enum_retailers_account_status 
   CHECK (account_status IN ('Unregistered', 'RegisteredInactive', 'RegisteredActive', 'PausedByRequest', 'PausedByBilling', 'Deactivated') );