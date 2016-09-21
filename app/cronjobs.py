from django_cron import CronJobBase, Schedule


class ExampleCron(CronJobBase):
    RUN_EVERY_MINS = 60

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.cron.example_cron'

    def do(self):
        print 'Run cron'

