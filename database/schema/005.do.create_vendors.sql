create table if not exists vendors (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
	unregistered_vendor_retailer_id uuid NULL, 
    registered_replacement_vendor_id uuid NULL, 
    is_registered boolean NOT NULL DEFAULT FALSE,
	name varchar(255) NOT NULL,  
    hq_city  varchar(255) NULL,
    hq_state varchar(255) NULL,
    hq_country varchar(2),
    contact_email varchar(320) NULL, 
    contact_phone varchar(32) NULL, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   

CREATE INDEX IF NOT EXISTS idx_vendors_name ON public.vendors(name);  
CREATE INDEX IF NOT EXISTS idx_vendors_is_registered ON public.vendors(is_registered);
CREATE INDEX IF NOT EXISTS idx_vendors_unregistered_vendor_retailer_id ON public.vendors(unregistered_vendor_retailer_id);
CREATE INDEX IF NOT EXISTS idx_vendors_registered_replacement_vendor_id ON public.vendors(registered_replacement_vendor_id);
CREATE INDEX IF NOT EXISTS idx_vendors_hq_city ON public.vendors(hq_city); 
CREATE INDEX IF NOT EXISTS idx_vendors_hq_state ON public.vendors(hq_state); 
CREATE INDEX IF NOT EXISTS idx_vendors_hq_country ON public.vendors(hq_country); 
CREATE INDEX IF NOT EXISTS idx_vendors_created_at ON public.vendors(created_at); 