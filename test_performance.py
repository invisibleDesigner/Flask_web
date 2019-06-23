import app
from routes.index import user_detail
import cProfile
from pstats import Stats


def profile_request(path, cookie, f):
    a = app.configured_app()
    pr = cProfile.Profile()
    headers = {'Cookie': cookie}

    with a.test_request_context(path, headers=headers):
        pr.enable()

        # r = f()
        # assert type(r) == str, r
        f(1)

        pr.disable()

    # pr.dump_stats('gua_profile.out')
    # pr.create_stats()
    # s = Stats(pr)
    pr.create_stats()
    s = Stats(pr).sort_stats('cumulative')
    s.dump_stats('user_detail.pstat')

    s.print_stats('.*pyForum.*')
    # s.print_callers()


if __name__ == '__main__':
    path = '/user/1'
    cookie = 'session=eyJfcGVybWFuZW50Ijp0cnVlLCJ1c2VyX2lkIjoyfQ.XCN9nQ.YgXb1Twz5E8pdwfkeojXI5R2QPI'
    profile_request(path, cookie, user_detail)

