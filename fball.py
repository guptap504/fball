import requests
import json
import argparse
from tabulate import tabulate


url = 'http://api.football-data.org/v1/competitions/'
params = {'season': 2018}
headers = {'X-Auth-Token': ''}


def show_codes(year=2018):
    params['season'] = year
    response = requests.get(url=url, params=params, headers=headers)
    jdata = json.loads(response.content)
    for leagues in jdata:
        print('{}, {}'.format(leagues['caption'], leagues['league']))

def world_cup(jdata):
    for key in jdata['standings'].keys():
        print('Group ', key)
        stand = []
        for team in jdata['standings'][key]:
            stand.append([team['rank'], team['team'], team['goalDifference'], team['points']])
        print(tabulate(stand, headers=['Rank', 'Team', 'GD', 'Points']))

def get_standings(league, season):
    params['season'] = season
    response = requests.get(url=url, params=params, headers=headers)
    jdata = json.loads(response.content)
    for leagues in jdata:
        if leagues['league'] == league:
            url1 = leagues['_links']['leagueTable']['href']
            response = requests.get(url=url1, params=None, headers=headers)
            jdata = json.loads(response.content)
            #print(json.dumps(jdata, indent=5, sort_keys=True))
            print(jdata['leagueCaption'])
            print('Current match day = ', jdata['matchday'])

            if leagues['league'] == "WC": world_cup(jdata)
            else:
                stand = []
                for t in jdata['standing']:
                    team = [t['position'], t['teamName'], t['goalDifference'], t['points']]
                    stand.append(team)
                print(tabulate(stand, headers=['Rank', 'Team', 'GD', 'Points']))
            return
    print('Incorrect league/season')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--list', help='List the competitions. Use with --season for specific season (default: current season)', action='store_true')
    parser.add_argument('--league', help='Select league', type=str)
    parser.add_argument('--season', help='Select season', type=int)
    parser.add_argument('--scores', help='Get scores', action='store_true')
    parser.add_argument(
        '--fixtures', help='Upcoming fixtures', action='store_true')
    parser.add_argument(
        '--standings', help='Get league standings', action='store_true')
    args = parser.parse_args()
    if args.list:
        if args.season:
            show_codes(args.season)
        else:
            show_codes()
    elif args.standings:
        if len(args.league) == 0:
            print(parser.print_help())
        elif args.season == 0:
            print(parser.print_help())
        get_standings(args.league, args.season)


if __name__ == "__main__":
    main()
