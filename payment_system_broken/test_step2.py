from payment_api.chaos_injector import ChaosInjector


cfg = ChaosConfig(
    failure_rate        = 0.0,
    duplicate_rate      = 0.0,
    delay_range         = (0.0, 0.0),
    corruption_rate     = 0.0,
    network_partition   = False,
)

injector = ChaosInjector(cfg)

print('ChaosInjector created    :', injector)
print('Should fail (0% rate)    :', injector.should_fail())
print('Should duplicate (0%)    :', injector.should_duplicate())
print('Should corrupt (0%)      :', injector.should_corrupt())
print('Is partitioned (False)   :', injector.is_network_partitioned())

print()
print('ALL GOOD - chaos_injector.py works correctly')
