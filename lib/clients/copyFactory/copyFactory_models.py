from typing_extensions import TypedDict
from typing import List, Optional
from datetime import datetime
from enum import Enum


CopyFactoryStrategySymbolMapping = TypedDict(
    "CopyFactoryStrategySymbolMapping",
    {
        "from": str,  # Symbol name to convert from.
        "to": str  # Symbol name to convert to.
    }
)
"""CopyFactory strategy symbol mapping."""


class CopyFactoryStrategyIdAndName(TypedDict):
    """CopyFactory strategy id and name."""
    id: str
    """Unique strategy id."""
    name: str
    """Human-readable strategy name."""


class CopyFactoryStrategyStopout(TypedDict):
    """CopyFactory strategy stopout."""
    strategy: CopyFactoryStrategyIdAndName
    """Strategy which was stopped out."""
    reason: str
    """Stopout reason. One of yearly-balance, monthly-balance, daily-balance, yearly-equity, monthly-equity,
    daily-equity, max-drawdown"""
    reasonDescription: str
    """Human-readable description of the stopout reason."""
    stoppedAt: datetime
    """Time the strategy was stopped at."""
    stoppedTill: datetime
    """Time the strategy is stopped till."""


class CopyFactoryStrategyEquityCurveFilter(TypedDict):
    """CopyFactory strategy equity curve filter."""
    period: float
    """Moving average period, must be greater or equal to 1."""
    granularity: str
    """Moving average granularity, a positive integer followed by time unit, e.g. 2h.
    Allowed units are s, m, h, d and w."""


class StrategyId(TypedDict):
    """Strategy id"""
    id: str
    """Strategy id"""


class CopyFactoryStrategyStopOutSettings(TypedDict):
    """CopyFactory strategy stopout settings."""
    value: float
    """Value of the stop out risk, expressed as a fraction of 1."""
    startTime: Optional[datetime]
    """The time to start risk calculation from. All previous trades will be ignored. You can use it to reset the risk
    counter after a stopout event."""


class CopyFactoryStrategySymbolFilter(TypedDict):
    """CopyFactory symbol filter."""
    included: List[str]
    """List of symbols copied. Leave the value empty to copy all symbols."""
    excluded: List[str]
    """List of symbols excluded from copying. Leave the value empty to copy all symbols."""


class CopyFactoryStrategyBreakingNewsFilter(TypedDict):
    """CopyFactory breaking news risk filter."""
    priorities: List[str]
    """List of breaking news priorities to stop trading on, leave empty to disable breaking news filter. One of high,
    medium, low."""
    closePositionTimeGapInMinutes: Optional[float]
    """Optional time interval specifying when to force close an already open position before calendar news. Default
    value is 60 minutes."""
    openPositionFollowingTimeGapInMinutes: Optional[float]
    """Optional time interval specifying when it is allowed to open position after calendar news. Default value is
    60 minutes."""


class CopyFactoryStrategyCalendarNewsFilter(TypedDict):
    """CopyFactory calendar news filter."""
    priorities: List[str]
    """List of calendar news priorities to stop trading on, leave empty to disable calendar news filter. One of
    election, high, medium, low."""
    closePositionTimeGapInMinutes: Optional[float]
    """Optional time interval specifying when to force close an already open position before calendar news. Default
    value is 60 minutes."""
    openPositionPrecedingTimeGapInMinutes: Optional[float]
    """Optional time interval specifying when it is still allowed to open position before calendar news. Default value
    is 120 minutes."""
    openPositionFollowingTimeGapInMinutes: Optional[float]
    """Optional time interval specifying when it is allowed to open position after calendar news. Default value is 60
    minutes"""


class CopyFactoryStrategyNewsFilter(TypedDict):
    """CopyFactory news risk filter."""
    breakingNewsFilter: Optional[CopyFactoryStrategyBreakingNewsFilter]
    """Optional breaking news filter."""
    calendarNewsFilter: Optional[CopyFactoryStrategyCalendarNewsFilter]
    """Optional calendar news filter."""


class CopyFactoryStrategyMaxStopLoss(TypedDict):
    """CopyFactory strategy max stop loss settings."""
    value: float
    """Maximum SL value."""
    units: str
    """SL units. Only pips value is supported at this point."""


class CopyFactoryStrategyRiskLimit(TypedDict):
    """CopyFactory risk limit filter."""
    type: str
    """Restriction type. One of daily, monthly, or yearly."""
    applyTo: str
    """Account metric to apply limit to. One of balance, equity."""
    maxRisk: float
    """Max drawdown allowed, expressed as a fraction of 1."""
    closePositions: bool
    """Whether to force close positions when the risk is reached. If value is false then only the new trades will be
    halted, but existing ones will not be closed"""
    startTime: Optional[datetime]
    """Optional time to start risk tracking from. All previous trades will be ignored. You can use this value to reset
    the filter after stopout event."""


class CopyFactoryStrategySubscription(TypedDict):
    """CopyFactory strategy subscriptions."""
    strategyId: str
    """Id of the strategy to subscribe to."""
    multiplier: Optional[float]
    """Optional subscription multiplier, default is 1x."""
    skipPendingOrders: Optional[bool]
    """Optional flag indicating that pending orders should not be copied. Default is to copy pending orders."""
    closeOnly: Optional[str]
    """Optional setting which instructs the application not to open new positions. by-symbol means that it is still
    allowed to open new positions with a symbol equal to the symbol of an existing strategy position (can be used to
    gracefully exit strategies trading in netting mode or placing a series of related trades per symbol). One of
    by-position, by-symbol or leave empty to disable this setting."""
    maxTradeRisk: Optional[float]
    """Optional max risk per trade, expressed as a fraction of 1. If trade has a SL, the trade size will be adjusted to
    match the risk limit. If not, the trade SL will be applied according to the risk limit."""
    reverse: bool
    """Flag indicating that the strategy should be copied in a reverse direction."""
    reduceCorrelations: Optional[str]
    """Optional setting indicating whether to enable automatic trade correlation reduction. Possible settings are not
    specified (disable correlation risk restrictions), by-strategy (limit correlations on strategy level) or by-symbol
    (limit correlations on symbol level)."""
    stopOutRisk: Optional[CopyFactoryStrategyStopOutSettings]
    """Optional stop out setting. All trading will be terminated and positions closed once equity drawdown reaches
    this value."""
    symbolFilter: Optional[CopyFactoryStrategySymbolFilter]
    """Optional symbol filter which can be used to copy only specific symbols or exclude some symbols from copying."""
    newsFilter: Optional[CopyFactoryStrategyNewsFilter]
    """Optional news risk filter configuration."""
    riskLimits: Optional[List[CopyFactoryStrategyRiskLimit]]
    """Optional strategy risk limits. You can configure trading to be stopped once total drawdown generated during
    specific period is exceeded. Can be specified either for balance or equity drawdown."""
    maxStopLoss: Optional[CopyFactoryStrategyMaxStopLoss]
    """Optional stop loss value restriction."""
    maxLeverage: Optional[float]
    """Optional setting indicating maximum leverage allowed when opening a new positions. Any trade which results in a
    higher leverage will be discarded."""
    symbolMapping: Optional[List[CopyFactoryStrategySymbolMapping]]
    """Defines how symbol name should be changed when trading (e.g. when broker uses symbol names with unusual
    suffixes). By default this setting is disabled and the trades are copied using signal source symbol name."""
    tradeSizeScalingMode: Optional[str]
    """If set to balance, the trade size on strategy subscriber will be scaled according to balance to preserve risk.
    If value is none, then trade size will be preserved irregardless of the subscriber balance. If value is
    contractSize, then trade size will be scaled according to contract size. Default is balance."""


class CopyFactoryAccountUpdate(TypedDict):
    """CopyFactory account update."""
    name: str
    """Account human-readable name."""
    connectionId: str
    """Id of the MetaApi MetaTrader account this copy trading account is connected to."""
    reservedMarginFraction: Optional[float]
    """Optional fraction of reserved margin to reduce a risk of margin call. Default is to reserve no margin. We
    recommend using maxLeverage setting instead. Specified as a fraction of balance thus the value is usually greater
    than 1."""
    phoneNumbers: Optional[List[str]]
    """Optional phone numbers to send sms notifications to. Leave empty to receive no sms notifications."""
    minTradeAmount: Optional[float]
    """Optional value of minimal trade size allowed, expressed in amount of account currency. Can be useful if your
    broker charges a fixed fee per transaction so that you can skip small trades with high broker commission rates.
    Default is 100."""
    closeOnly: Optional[str]
    """Optional setting wich instructs the application not to open new positions. by-symbol means that it is still
    allowed to open new positions with a symbol equal to the symbol of an existing strategy position (can be used to
    gracefully exit strategies trading in netting mode or placing a series of related trades per symbol). One of
    by-position, by-symbol or leave empty to disable this setting."""
    stopOutRisk: Optional[CopyFactoryStrategyStopout]
    """Optional stop out setting. All trading will be terminated and positions closed once equity drawdown reaches
    this value."""
    riskLimits: Optional[List[CopyFactoryStrategyRiskLimit]]
    """Optional account risk limits. You can configure trading to be stopped once total drawdown generated during
    specific period is exceeded. Can be specified either for balance or equity drawdown."""
    maxLeverage: Optional[float]
    """Optional setting indicating maxumum leverage allowed when opening a new positions. Any trade which results in a
    higher leverage will be discarded."""
    subscriptions: List[CopyFactoryStrategySubscription]
    """Strategy subscriptions."""


class CopyFactoryAccount(CopyFactoryAccountUpdate):
    """CopyFactory account model."""
    _id: str
    """Account unique identifier."""


class CopyFactoryStrategy(TypedDict):
    """CopyFactory provider strategy"""
    _id: str
    """Unique strategy id."""
    platformCommissionRate: float
    """Commission rate the platform charges for strategy copying, applied to commissions charged by provider. This
    commission applies only to accounts not managed directly by provider. Should be a fraction of 1."""


class CopyFactoryStrategyCommissionScheme(TypedDict):
    """CopyFactory strategy commission scheme."""
    type: str
    """Commission type. One of flat-fee, lots-traded, lots-won, amount-traded, amount-won, high-water-mark."""
    billingPeriod: str
    """Billing period. One of week, month, quarter."""
    commissionRate: float
    """Commission rate. Should be greater than or equal to zero if commission type is flat-fee, lots-traded or
    lots-won, should be greater than or equal to zero and less than or equal to 1 if commission type is amount-traded,
    amount-won, high-water-mark."""


class CopyFactoryStrategyMagicFilter(TypedDict):
    """CopyFactory strategy magic filter."""
    included: List[str]
    """List of magics (expert ids) or magic ranges copied. Leave the value empty to copy all magics."""
    excluded: List[str]
    """List of magics (expert ids) or magic ranges excluded from copying. Leave the value empty to copy all magics."""


class CopyFactoryStrategyTimeSettings(TypedDict):
    """CopyFactory strategy time settings."""
    lifetimeInHours: Optional[float]
    """Optional position lifetime. Default is to keep positions open up to 90 days."""
    openingIntervalInMinutes: Optional[float]
    """Optional time interval to copy new positions. Default is to let 1 minute for the position to get copied. If
    position were not copied during this time, the copying will not be retried anymore."""


class CopyFactoryStrategyUpdate(TypedDict):
    """CopyFactory strategy update."""
    name: str
    """Strategy human-readable name."""
    description: str
    """Longer strategy human-readable description."""
    positionLifecycle: str
    """Position detection mode. Allowed values are netting (single position per strategy per symbol),
    hedging (multiple positions per strategy per symbol)"""
    connectionId: str
    """Id of the MetaApi account providing the strategy."""
    skipPendingOrders: Optional[bool]
    """Optional flag indicating that pending orders should not be copied. Default is to copy pending orders"""
    commissionScheme: Optional[CopyFactoryStrategyCommissionScheme]
    """Commission scheme allowed by this strategy."""
    platformCommissionRate: float
    """Commission rate the platform charges for strategy copying, applied to commissions charged by provider. This
    commission applies only to accounts not managed directly by provider. Should be fraction of 1."""
    maxTradeRisk: Optional[float]
    """Optional max risk per trade, expressed as a fraction of 1. If trade has a SL, the trade size will be adjusted to
    match the risk limit. If not, the trade SL will be applied according to the risk limit."""
    reverse: bool
    """Flag indicating that the strategy should be copied in a reverse direction."""
    reduceCorrelations: Optional[str]
    """Optional setting indicating whether to enable automatic trade correlation reduction. Possible settings are not
    specified (disable correlation risk restrictions), by-strategy (limit correlations on strategy level) or by-symbol
    (limit correlations on symbol level)."""
    stopOutRisk: Optional[CopyFactoryStrategyStopOutSettings]
    """Optional stop out setting. All trading will be terminated and positions closed once equity drawdown reaches
    this value."""
    symbolFilter: Optional[CopyFactoryStrategySymbolFilter]
    """Symbol filters which can be used to copy only specific symbols or exclude some symbols from copying."""
    newsFilter: Optional[CopyFactoryStrategyNewsFilter]
    """News risk filter configuration."""
    riskLimits: Optional[List[CopyFactoryStrategyRiskLimit]]
    """Optional strategy risk limits. You can configure trading to be stopped once total drawdown generated during
    specific period is exceeded. Can be specified either for balance or equity drawdown."""
    maxStopLoss: Optional[CopyFactoryStrategyMaxStopLoss]
    """Optional stop loss value restriction."""
    maxLeverage: Optional[float]
    """Optional max leverage risk restriction. All trades resulting in a leverage value higher than specified will
    be skipped."""
    magicFilter: Optional[CopyFactoryStrategyMagicFilter]
    """Optional magic (expert id) filter."""
    timeSettings: Optional[CopyFactoryStrategyTimeSettings]
    """Settings to manage copying timeframe and position lifetime. Default is to copy position within 1 minute from
    being opened at source and let the position to live for up to 90 days."""
    symbolMapping: Optional[List[CopyFactoryStrategySymbolMapping]]
    """Defines how symbol name should be changed when trading (e.g. when broker uses symbol names with unusual
    suffixes). By default this setting is disabled and the trades are copied using signal source symbol name."""
    tradeSizeScalingMode: Optional[str]
    """If set to balance, the trade size on strategy subscriber will be scaled according to balance to preserve risk.
    If value is none, then trade size will be preserved irregardless of the subscriber balance. If value is
    contractSize, then trade size will be scaled according to contract size. Default is balance."""
    equityCurveFilter: CopyFactoryStrategyEquityCurveFilter
    """Filter which permits the trades only if account equity is greater than balance moving average."""


class CopyFactorySubscriberOrProvider(TypedDict):
    """CopyFactory provider or subscriber"""
    id: str
    """Profile id."""
    name: str
    """User name."""
    strategies: List[CopyFactoryStrategyIdAndName]
    """Array of strategy IDs provided by provider or subscribed to by subscriber."""


class CopyFactoryTransactionMetrics(TypedDict):
    """Trade copying metrics such as slippage and latencies."""
    tradeCopyingLatency: Optional[float]
    """Trade copying latency, measured in milliseconds based on transaction time provided by broker."""
    tradeCopyingSlippageInBasisPoints: Optional[float]
    """Trade copying slippage, measured in basis points (0.01 percent) based on transaction price provided by broker."""
    tradeCopyingSlippageInAccountCurrency: Optional[float]
    """Trade copying slippage, measured in account currency based on transaction price provided by broker."""
    mtAndBrokerSignalLatency: Optional[float]
    """Trade signal latency introduced by broker and MT platform, measured in milliseconds."""
    tradeAlgorithmLatency: Optional[float]
    """Trade algorithm latency introduced by CopyFactory servers, measured in milliseconds."""
    mtAndBrokerTradeLatency: Optional[float]
    """Trade latency for a copied trade introduced by broker and MT platform, measured in milliseconds"""
    totalLatency: Optional[float]
    """Total trade copying latency, measured in milliseconds. This value might be slightly different from
    tradeCopyingLatency value due to limited measurement precision as it is measured based on timestamps captured
    during copy trading process as opposed to broker data"""


class CopyFactoryTransaction(TypedDict):
    """CopyFactory transaction."""
    id: str
    """Transaction id."""
    type: str
    """Transaction type (one of DEAL_TYPE_BUY, DEAL_TYPE_SELL, DEAL_TYPE_BALANCE, DEAL_TYPE_CREDIT, DEAL_TYPE_CHARGE,
    DEAL_TYPE_CORRECTION, DEAL_TYPE_BONUS, DEAL_TYPE_COMMISSION, DEAL_TYPE_COMMISSION_DAILY,
    DEAL_TYPE_COMMISSION_MONTHLY, DEAL_TYPE_COMMISSION_AGENT_DAILY, DEAL_TYPE_COMMISSION_AGENT_MONTHLY,
    DEAL_TYPE_INTEREST, DEAL_TYPE_BUY_CANCELED, DEAL_TYPE_SELL_CANCELED, DEAL_DIVIDEND, DEAL_DIVIDEND_FRANKED,
    DEAL_TAX). See https://www.mql5.com/en/docs/constants/tradingconstants/dealproperties#enum_deal_type."""
    time: datetime
    """Transaction time."""
    accountId: str
    """CopyFactory account id."""
    symbol: Optional[str]
    """Optional symbol traded."""
    subscriber: CopyFactorySubscriberOrProvider
    """Strategy subscriber."""
    demo: bool
    """Demo account flag."""
    provider: CopyFactorySubscriberOrProvider
    """Strategy provider."""
    strategy: CopyFactoryStrategyIdAndName
    """Strategy."""
    positionId: Optional[str]
    """Source position id."""
    improvement: float
    """High-water mark strategy balance improvement."""
    providerCommission: float
    """Provider commission."""
    platformCommission: float
    """Platform commission."""
    incomingProviderCommission: Optional[float]
    """Commission paid by provider to underlying providers."""
    incomingPlatformCommission: Optional[float]
    """Platform commission paid by provider to underlying providers."""
    lotPrice: Optional[float]
    """Trade lot price."""
    tickPrice: Optional[float]
    """Trade tick price."""
    amount: Optional[float]
    """Trade amount."""
    commission: Optional[float]
    """Trade commission."""
    swap: float
    """Trade swap."""
    profit: float
    """Trade profit."""
    metrics: Optional[CopyFactoryTransactionMetrics]
    """trade copying metrics such as slippage and latencies. Measured selectively for copied trades"""


class ResynchronizationTask(TypedDict):
    """Resynchronization task."""
    _id: str
    """Task unique id."""
    type: str
    """Task type. One of CREATE_ACCOUNT, CREATE_STRATEGY, UPDATE_STRATEGY, REMOVE_STRATEGY."""
    createdAt: datetime
    """The time task was created at."""
    status: str
    """Task status. One of PLANNED, EXECUTING, SYNCHRONIZING."""


class CopyFactoryPortfolioMember(TypedDict):
    """Portfolio strategy member."""
    strategyId: str
    """Member strategy id."""
    multiplier: float
    """Copying multiplier (weight in the portfolio)."""
    skipPendingOrders: Optional[bool]
    """Optional flag indicating that pending orders should not be copied. Default is to copy pending orders."""
    maxTradeRisk: Optional[float]
    """Optional max risk per trade, expressed as a fraction of 1. If trade has a SL, the trade size will be adjusted
    to match the risk limit. If not, the trade SL will be applied according to the risk limit."""
    reverse: bool
    """Flag indicating that the strategy should be copied in a reverse direction."""
    reduceCorrelations: Optional[str]
    """Optional setting indicating whether to enable automatic trade correlation reduction. Possible settings are
    not specified (disable correlation risk restrictions), by-strategy (limit correlations on strategy level) or
    by-symbol (limit correlations on symbol level)."""
    stopOutRisk: Optional[CopyFactoryStrategyStopOutSettings]
    """Optional stop out setting. All trading will be terminated and positions closed once equity drawdown reaches this
    value."""
    symbolFilter: Optional[CopyFactoryStrategySymbolFilter]
    """Symbol filters which can be used to copy only specific symbols or exclude some symbols from copying."""
    newsFilter: Optional[CopyFactoryStrategyNewsFilter]
    """News risk filter configuration."""
    riskLimits: Optional[List[CopyFactoryStrategyRiskLimit]]
    """Optional strategy risk limits. You can configure trading to be stopped once total drawdown generated during
    specific period is exceeded. Can be specified either for balance or equity drawdown."""
    maxStopLoss: Optional[CopyFactoryStrategyMaxStopLoss]
    """Optional stop loss value restriction."""
    maxLeverage: Optional[float]
    """Optional max leverage risk restriction. All trades resulting in a leverage value higher than specified will be
    skipped."""
    symbolMapping: Optional[List[CopyFactoryStrategySymbolMapping]]
    """Defines how symbol name should be changed when trading (e.g. when broker uses symbol names with unusual
    suffixes). By default this setting is disabled and the trades are copied using signal source symbol name."""
    tradeSizeScalingMode: Optional[str]
    """If set to balance, the trade size on strategy subscriber will be scaled according to balance to preserve risk.
    If value is none, then trade size will be preserved irregardless of the subscriber balance. If value is
    contractSize, then trade size will be scaled according to contract size. Default is balance."""


class CopyFactoryPortfolioStrategyUpdate(TypedDict):
    """Portfolio strategy update."""
    name: str
    """Strategy human-readable name."""
    description: str
    """Longer strategy human-readable description."""
    members: List[CopyFactoryPortfolioMember]
    """Array of portfolio memebers."""
    commissionScheme: Optional[CopyFactoryStrategyCommissionScheme]
    """Commission scheme allowed by this strategy. By default monthly billing period with no commission is being
    used."""
    skipPendingOrders: Optional[bool]
    """Optional flag indicating that pending orders should not be copied. Default is to copy pending orders."""
    maxTradeRisk: Optional[float]
    """Optional max risk per trade, expressed as a fraction of 1. If trade has a SL, the trade size will be adjusted
    to match the risk limit. If not, the trade SL will be applied according to the risk limit."""
    reverse: bool
    """Flag indicating that the strategy should be copied in a reverse direction."""
    reduceCorrelations: Optional[str]
    """Optional setting indicating whether to enable automatic trade correlation reduction. Possible settings are not
    specified (disable correlation risk restrictions), by-strategy (limit correlations on strategy level) or by-symbol
    (limit correlations on symbol level)."""
    stopOutRisk: Optional[CopyFactoryStrategyStopOutSettings]
    """Optional stop out setting. All trading will be terminated and positions closed once equity drawdown reaches this
    value."""
    symbolFilter: Optional[CopyFactoryStrategySymbolFilter]
    """Symbol filters which can be used to copy only specific symbols or exclude some symbols from copying."""
    newsFilter: Optional[CopyFactoryStrategyNewsFilter]
    """News risk filter configuration."""
    riskLimits: Optional[List[CopyFactoryStrategyRiskLimit]]
    """Optional strategy risk limits. You can configure trading to be stopped once total drawdown generated during
    specific period is exceeded. Can be specified either for balance or equity drawdown."""
    maxStopLoss: Optional[CopyFactoryStrategyMaxStopLoss]
    """Optional stop loss value restriction."""
    maxLeverage: Optional[float]
    """Optional max leverage risk restriction. All trades resulting in a leverage value higher than specified will be
    skipped."""
    symbolMapping: Optional[List[CopyFactoryStrategySymbolMapping]]
    """Defines how symbol name should be changed when trading (e.g. when broker uses symbol names with unusual
    suffixes). By default this setting is disabled and the trades are copied using signal source symbol name."""
    tradeSizeScalingMode: Optional[str]
    """If set to balance, the trade size on strategy subscriber will be scaled according to balance to preserve risk.
    If value is none, then trade size will be preserved irregardless of the subscriber balance. If value is
    contractSize, then trade size will be scaled according to contract size. Default is balance."""


class CopyFactoryPortfolioStrategy(CopyFactoryPortfolioStrategyUpdate):
    """Portfolio strategy, i.e. the strategy which includes a set of other strategies."""
    _id: str
    """Unique strategy id."""
    platformCommissionRate: float
    """Commission rate the platform charges for strategy copying, applied to commissions charged by provider. This
    commission applies only to accounts not managed directly by provider. Should be fraction of 1."""


class LogLevel(Enum):
    """Log level."""
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'


class CopyFactoryUserLogRecord(TypedDict):
    """Trade copying user log record."""
    time: datetime
    """Log record time."""
    level: LogLevel
    """Log level. One of INFO, WARN, ERROR."""
    message: str
    """Log message."""
    symbol: Optional[str]
    """Symbol traded."""
    strategyId: Optional[str]
    """Id of the strategy event relates to."""
    strategyName: Optional[str]
    """Name of the strategy event relates to."""
    positionId: Optional[str]
    """Position id event relates to."""
    side: Optional[str]
    """Side of the trade event relates to. One of buy, sell, close."""
    type: Optional[str]
    """Type of the trade event relates to. One of market, limit, stop."""
    openPrice: Optional[float]
    """Open price for limit and stop orders."""
