create table if not exists inventory_product_snapshots (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
	product_id uuid NOT NULL, 
	retailer_id uuid NOT NULL, 
	retailer_location_id uuid NOT NULL, 
  vendor_id uuid NULL, 
  inventory_intake_job_id uuid NULL,
  snapshot_hour timestamptz(3)  NOT NULL , 
  sku varchar(255) NOT NULL,
  stock_on_hand integer NOT NULL,
  price integer NOT NULL,
  lot_identifier varchar(255) NULL,    
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);

CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_product_id ON public.inventory_product_snapshots(product_id);   
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_retailer_id ON public.inventory_product_snapshots(retailer_id);   
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_retailer_location_id ON public.inventory_product_snapshots(retailer_location_id);
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_vendor_id ON public.inventory_product_snapshots(vendor_id);
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_inventory_intake_job_id ON public.inventory_product_snapshots(inventory_intake_job_id); 
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_lot_identifier ON public.inventory_product_snapshots(lot_identifier); 
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_snapshot_hour ON public.inventory_product_snapshots(snapshot_hour);
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_sku ON public.inventory_product_snapshots(sku);
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_sku_and_lot_identifier ON public.inventory_product_snapshots(sku, lot_identifier);
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_retailer_location_id_and_snapshot_hour ON public.inventory_product_snapshots(retailer_location_id, snapshot_hour);
CREATE INDEX IF NOT EXISTS idx_inventory_product_snapshots_retailer_location_id_and_product_id_and_snapshot_hour ON public.inventory_product_snapshots(retailer_location_id, product_id, snapshot_hour);
 
-- FKs

ALTER TABLE public.inventory_product_snapshots DROP CONSTRAINT IF EXISTS fk_inventory_product_snapshots_product_id;

ALTER TABLE public.inventory_product_snapshots
  ADD CONSTRAINT fk_inventory_product_snapshots_product_id
  FOREIGN KEY (product_id)
  REFERENCES public.products(id);

ALTER TABLE public.inventory_product_snapshots DROP CONSTRAINT IF EXISTS fk_inventory_product_snapshots_retailer_id;

ALTER TABLE public.inventory_product_snapshots
  ADD CONSTRAINT fk_inventory_product_snapshots_retailer_id
  FOREIGN KEY (retailer_id)
  REFERENCES public.retailers(id);

ALTER TABLE public.inventory_product_snapshots DROP CONSTRAINT IF EXISTS fk_inventory_product_snapshots_retailer_location_id;

ALTER TABLE public.inventory_product_snapshots
  ADD CONSTRAINT fk_inventory_product_snapshots_retailer_location_id
  FOREIGN KEY (retailer_location_id)
  REFERENCES public.retailer_locations(id);

ALTER TABLE public.inventory_product_snapshots DROP CONSTRAINT IF EXISTS fk_inventory_product_snapshots_referring_vendor_id;

ALTER TABLE public.inventory_product_snapshots
  ADD CONSTRAINT fk_inventory_product_snapshots_referring_vendor_id
  FOREIGN KEY (vendor_id)
  REFERENCES public.vendors(id);

ALTER TABLE public.inventory_product_snapshots DROP CONSTRAINT IF EXISTS fk_inventory_product_snapshots_intake_job_id;

ALTER TABLE public.inventory_product_snapshots
  ADD CONSTRAINT fk_inventory_product_snapshots_intake_job_id
  FOREIGN KEY (inventory_intake_job_id)
  REFERENCES public.inventory_intake_jobs(id);