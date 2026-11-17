namespace cost;

entity CostCenters {
  key ID : String(10);
  name   : String(60);
}

entity Vendors {
  key ID : String(10);
  name   : String(60);
}

entity Projects {
  key ID     : String(10);
  name       : String(60);
  type       : String(10);
  startDate  : Date;
  costCenter : Association to CostCenters;
}

entity CostEntries {
  key project : Association to Projects;
  key period  : Date;
  actual      : Decimal(15,2);
  budget      : Decimal(15,2);
  currency    : String(3);
}

entity CapexStatus {
  key project    : Association to Projects;
  approvedBudget : Decimal(15,2);
  spentToDate    : Decimal(15,2);
  committed      : Decimal(15,2);
  progressPct    : Integer;
  status         : String(20);
  currency       : String(3);
}

entity Procurement {
  key prNumber : String(12);
  poNumber     : String(12);
  createdDate  : Date;
  prAmount     : Decimal(15,2);
  poAmount     : Decimal(15,2);
  status       : String(20);
  currency     : String(3);
  project      : Association to Projects;
  vendor       : Association to Vendors;
}
