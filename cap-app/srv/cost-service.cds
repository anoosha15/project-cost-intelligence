using cost as db from '../db/schema';

service CostService @(path: '/cost') {

  @readonly entity CostCenters as projection on db.CostCenters;
  @readonly entity Vendors     as projection on db.Vendors;
  @readonly entity Projects    as projection on db.Projects;

  // Monthly actual vs budget with variance
  @readonly entity CostVariance as select from db.CostEntries {
    key project.ID          as projectID,
    key period,
    project.name            as projectName,
    project.type            as projectType,
    project.costCenter.name as costCenterName,
    actual,
    budget,
    actual - budget         as variance : Decimal(15,2),
    case when budget = 0 then null
         else round((actual - budget) / budget * 100, 2)
    end                     as variancePct : Decimal(9,2),
    case when actual > budget then 1
         when actual < budget then 3
         else 0 end         as criticality : Integer,
    currency
  };

  // Capex status per project
  @readonly entity CapexOverview as select from db.CapexStatus {
    key project.ID as projectID,
    project.name   as projectName,
    approvedBudget,
    spentToDate,
    committed,
    approvedBudget - spentToDate - committed as remainingBudget : Decimal(15,2),
    progressPct,
    status,
    currency
  };

  // Purchase requisitions and orders
  @readonly entity ProcurementTracking as select from db.Procurement {
    key prNumber,
    poNumber,
    project.ID   as projectID,
    project.name as projectName,
    vendor.name  as vendorName,
    createdDate,
    prAmount,
    poAmount,
    status,
    case when status = 'Invoiced' then 'Closed' else 'Open' end as openClosed : String(10),
    currency
  };
}
