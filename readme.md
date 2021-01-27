# FTX Collateral Estimator

This tool helps assess USD collateral on FTX for cross-margin positions.

* Polygons are drawn if the USD collateral is below a certain threshold (specified as `collateral` in `main.py`)
* Positions are specified in `example.json`
    * `factor` specifies FTX weighting factor
    * `amount` is your current position at `price`
    * number of collateral assets is arbitrary

![Example Collateral Position](plot.png)
