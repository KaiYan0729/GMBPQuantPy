import pandas as pd
import gmbp_quant.common.unittest as ut
from gmbp_quant.apps.ipo.crawl_ipo_data import crawl_ipo_data_single_date


class TestCrawlIPOData(ut.TestCase):
    def test_crawl_ipo_data_single_date(self):
        dateid = 20210113
        target = crawl_ipo_data_single_date(dateid=dateid)
        benchmark = self.load_benchmark_dataframe(basename=f'ipo.{dateid}.csv')
        self.assertEqual(benchmark, target)
    #
#


if __name__ == '__main__':
    ut.main()
#
