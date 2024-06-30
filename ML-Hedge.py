from gs_quant.session import GsSession, Environment
GsSession.use(client_id=None, client_secret=None, scopes=('read_product_data',))

import datetime as dt
from gs_quant.markets.position_set import Position, PositionSe

positions = PositionSet(
        date=dt.date(day=24, month=9, year=2021),
        positions=[
            Position(identifier='AAPL UW', quantity=26),
            Position(identifier='GS UN', quantity=51)
        ]
    )

positions.resolve()

universe = ['SPX']

from gs_quant.markets.hedge import HedgeExclusions

exclusions = HedgeExclusions(assets=['GS UN'],
                             countries=['Mexico'],
                             regions=['Europe'],
                             sectors=['Utilities'],
                             industries=['Airlines'])


from gs_quant.markets.hedge import HedgeConstraints, Constraint,

constraints = HedgeConstraints(sectors=[Constraint(constraint_name='Software', minimum=0, maximum=20)],
                               esg=[Constraint(constraint_name='gPercentile', minimum=75, maximum=100)])


from gs_quant.markets.hedge import PerformanceHedgeParameters

parameters = PerformanceHedgeParameters(
    initial_portfolio=positions,
    universe=universe,
    exclusions=exclusions,
    constraints=constraints
)


from gs_quant.markets.hedge import HedgeConstraints, Constraint,

constraints = HedgeConstraints(sectors=[Constraint(constraint_name='Software', minimum=0, maximum=20)],
                               esg=[Constraint(constraint_name='gPercentile', minimum=75, maximum=100)])

from gs_quant.markets.hedge import PerformanceHedgeParameters

parameters = PerformanceHedgeParameters(
    initial_portfolio=positions,
    universe=universe,
    exclusions=exclusions,
    constraints=constraints
)


from gs_quant.markets.hedge import PerformanceHedge

hedge = PerformanceHedge(parameters)
all_results = hedge.calculate()

from IPython.display import display

hedge_constituents = hedge.get_constituents()
display(hedge_constituents)

backtest_performance = hedge.get_backtest_performance()

backtest_performance.plot(title='Backtest Performance')

from gs_quant.timeseries.helper import Window
from gs_quant.timeseries.econometrics import correlation

backtest_correlation = correlation(backtest_performance['Portfolio'], backtest_performance['Hedge'], Window(44, 0))
backtest_correlation.plot(title='Backtest Correlation')

positions = []
for index, row in hedge_constituents.iterrows():
    positions.append(Position(identifier=row['Bbid'], asset_id=row['Asset Id'], quantity=row['Shares']))

position_set = PositionSet(date=business_day_offset(dt.date.today(), -1, roll='forward'),
                           positions=positions)

from gs_quant.markets.portfolio import Portfolio
from gs_quant.markets.portfolio_manager import PortfolioManager

new_portfolio = Portfolio(name="Hedge as Portfolio")
new_portfolio.save()

pm = PortfolioManager(new_portfolio.id)
pm.update_positions([position_set])


from gs_quant.markets.baskets import Basket
from gs_quant.markets.indices_utils import ReturnType

my_basket = Basket()

my_basket.name = 'My New Custom Basket'
my_basket.ticker = 'GSMBXXXX'
my_basket.currency = 'USD'
my_basket.publish_to_reuters = True

my_basket.return_type = ReturnType.PRICE_RETURN

my_basket.position_set = position_set
my_basket.create()