using CostService as service from '../../srv/cost-service';

annotate service.CostVariance with {
  projectID      @Common.Label: 'Project';
  projectName    @Common.Label: 'Project Name';
  projectType    @Common.Label: 'Project Type';
  costCenterName @Common.Label: 'Cost Center';
  period         @Common.Label: 'Period';
  actual         @Common.Label: 'Actual';
  budget         @Common.Label: 'Budget';
  variance       @Common.Label: 'Variance';
  variancePct    @Common.Label: 'Variance %';
};

annotate service.CostVariance with @(
  UI.SelectionFields: [
    projectName,
    costCenterName,
    projectType
  ],
  UI.LineItem: [
    { Value: projectID,      ![@UI.Importance]: #Low },
    { Value: projectName,    ![@UI.Importance]: #High },
    { Value: costCenterName, ![@UI.Importance]: #Medium },
    { Value: period,         ![@UI.Importance]: #High },
    { Value: actual,         ![@UI.Importance]: #High },
    { Value: budget,         ![@UI.Importance]: #High },
    { Value: variance,       Criticality: criticality, ![@UI.Importance]: #High },
    { Value: variancePct,    ![@UI.Importance]: #High }
  ]
);