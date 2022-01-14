3.3.1
  - updated stopout settings and risk limit models

3.3.0
  - added remove_portfolio_strategy_member method
  - added closeOnRemovalMode to strategy, portfolio strategy and portfolio strategy member

3.2.0
  - added includeRemoved and pagination to get_strategies, get_portfolio_strategies, get_subscribers

3.1.6
  - added removeAfter field to closeInstructions

3.1.5
  - removed positionLifecycle property

3.1.4
  - updated docs

3.1.3
  - updated docs

3.1.2
  - updated dependencies

3.1.1
  - added subscriber profit field to trading signal model

3.1.0
  - fixed remove subscriber
  - added remove subscription method

3.0.2
  - updated remove REST API
  - updated StrategyStopout model

3.0.1
  - fixed transaction REST API

3.0.0
  - breaking change: migrated to CopyFactory 2

2.2.0
  - added drawdown filter
  - changed reduceCorrelations filter allowed values

2.1.0
  - added settings to disable SL and/or TP copying
  - added settings to specify max and min trade volume
  - added settings to configure trade size scaling

1.1.1
  - handle TooManyRequestsException in HTTP client

1.1.0
  - Added API to retrieve account / strategy / portfolio strategy by id

1.0.0
  - CopyFactory SDK is now a separate repository/module, migrated from metaapi.cloud python SDK
