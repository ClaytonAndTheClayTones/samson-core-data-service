create table if not exists products (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
	vendor_id uuid NULL, 
	referring_retailer_id uuid NULL, 
	referring_retailer_location_id uuid NULL, 
	confirmed_core_product_id uuid NULL, 
	vendor_confirmation_status varchar(32) NOT NULL DEFAULT 'Unknown', 
	name varchar(255) NOT NULL,     
	upc varchar(255) NULL, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);

CREATE INDEX IF NOT EXISTS idx_products_name ON public.products(name);  
CREATE INDEX IF NOT EXISTS idx_products_confirmed_core_product_id ON public.products(confirmed_core_product_id);   
CREATE INDEX IF NOT EXISTS idx_products_referring_retailer_id ON public.products(referring_retailer_id);   
CREATE INDEX IF NOT EXISTS idx_products_referring_retailer_location_id ON public.products(referring_retailer_location_id);   
CREATE INDEX IF NOT EXISTS idx_products_vendor_id ON public.products(vendor_id);   

CREATE INDEX IF NOT EXISTS idx_products_vendor_confirmation_status ON public.products(vendor_confirmation_status);  
CREATE INDEX IF NOT EXISTS idx_products_upc ON public.products(upc);  
 
-- Enums

ALTER TABLE public.products DROP CONSTRAINT IF EXISTS enum_products_account_status;
  
ALTER TABLE public.products  
   ADD CONSTRAINT enum_products_account_status 
   CHECK (vendor_confirmation_status IN ('Candidate', 'ConfirmedByVendor', 'DeniedByVendor', 'Discontinued', 'Unknown') );
 
-- FKs

ALTER TABLE public.products DROP CONSTRAINT IF EXISTS fk_products_confirmed_core_product_id;

ALTER TABLE public.products
  ADD CONSTRAINT fk_products_confirmed_core_product_id
  FOREIGN KEY (confirmed_core_product_id)
  REFERENCES public.products(id);

ALTER TABLE public.products DROP CONSTRAINT IF EXISTS fk_products_referring_retailer_id;

ALTER TABLE public.products
  ADD CONSTRAINT fk_products_referring_retailer_id
  FOREIGN KEY (referring_retailer_id)
  REFERENCES public.retailers(id);

  ALTER TABLE public.products DROP CONSTRAINT IF EXISTS fk_products_referring_retailer_location_id;

ALTER TABLE public.products
  ADD CONSTRAINT fk_products_referring_retailer_location_id
  FOREIGN KEY (referring_retailer_location_id)
  REFERENCES public.retailer_locations(id);

  ALTER TABLE public.products DROP CONSTRAINT IF EXISTS fk_products_vendor_id;

ALTER TABLE public.products
  ADD CONSTRAINT fk_products_vendor_id
  FOREIGN KEY (vendor_id)
  REFERENCES public.vendors(id);