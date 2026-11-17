sap.ui.define([
    "sap/fe/test/JourneyRunner",
	"costvariance/test/integration/pages/CostVarianceList.gen",
	"costvariance/test/integration/pages/CostVarianceObjectPage.gen"
], function (JourneyRunner, CostVarianceListGenerated, CostVarianceObjectPageGenerated) {
    'use strict';

    const runner = new JourneyRunner({
        launchUrl: sap.ui.require.toUrl('costvariance') + '/test/flp.html#app-preview',
        pages: {
			onTheCostVarianceListGenerated: CostVarianceListGenerated,
			onTheCostVarianceObjectPageGenerated: CostVarianceObjectPageGenerated
        },
        async: true
    });

    return runner;
});

