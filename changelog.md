6.0.0
  - add logs on retrieve stream errors
  - fixed FAQ URL
  - fixed strategy log stream job
  - breaking change: added strategyId, positionId, level params to subscriber logs search & streaming
  - breaking change: added positionId, level params to strategy logs search & streaming

5.11.0
  - added limit param to subscriber & strategy log streaming
  - fix subscriber & strategy extra log streaming after unsubscription
  - renamed expirePendingOrders -> expirePendingOrderSignals
  - made it possible to specify open price for market external signals

5.10.1
  - fixed signal client readme

5.10.0
  - make it possible to stream user logs and transactions
  - make it possible to delay trading signals by configured amount of time
  - updated trade size scaling expression variables
  - added equity trade size scaling mode
  - added expression option to strategy trade size scaling

5.6.0
  - make it possible to expire pending order signals

5.5.2
  - fixed dependency vulnerabilities

5.5.1
  - updated telegram integration documentation

5.5.0
  - refactored risk limits (please make sure to update your apps to use new enumerations)

5.4.0
  - expanded strategy trade size scaling options

5.3.0
  - added telegram integration

5.2.1
  - added references to MT manager api and risk management api

5.2.0
  - added get_strategy_log method

5.1.0
  - removed stop out risk from models
  - added stopout listener
  - breaking change: signal methods moved to a separate class
  - implemented region support
  
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
