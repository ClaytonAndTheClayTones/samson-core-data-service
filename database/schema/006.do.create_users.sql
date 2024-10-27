create table if not exists users (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
	vendor_id uuid NULL, 
	retailer_location_id uuid NULL, 
    retailer_id uuid NULL,  
	first_name varchar(64) NOT NULL, 
	last_name varchar(64) NOT NULL,  
    full_name varchar(255) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,  
    role varchar(64) NOT NULL, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
 
CREATE INDEX IF NOT EXISTS idx_users_role ON public.users(role);
CREATE INDEX IF NOT EXISTS idx_users_full_name ON public.users(full_name);
CREATE INDEX IF NOT EXISTS idx_users_retailer_id ON public.users(retailer_id);
CREATE INDEX IF NOT EXISTS idx_users_vendor_id ON public.users(vendor_id); 
CREATE INDEX IF NOT EXISTS idx_users_retailer_location_id ON public.users(retailer_location_id); 
CREATE INDEX IF NOT EXISTS idx_users_created_at ON public.users(created_at); 

ALTER TABLE public.users DROP CONSTRAINT IF EXISTS fk_users_retailer_id;

ALTER TABLE public.users
  ADD CONSTRAINT fk_users_retailer_id
  FOREIGN KEY (retailer_id)
  REFERENCES public.retailers(id);

ALTER TABLE public.users DROP CONSTRAINT IF EXISTS fk_users_retailer_location_id;

ALTER TABLE public.users
  ADD CONSTRAINT fk_users_retailer_location_id
  FOREIGN KEY (retailer_location_id)
  REFERENCES public.retailer_locations(id);

ALTER TABLE public.users DROP CONSTRAINT IF EXISTS fk_users_vendor_id;

ALTER TABLE public.users
  ADD CONSTRAINT fk_users_vendor_id
  FOREIGN KEY (vendor_id)
  REFERENCES public.vendors(id); 