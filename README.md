# Data Engineering Support Rota

This tool pairs up team members and schedules them to work support for the data engineering team. The support rota is made available in a Google Calendar.

## Usage

WARNING :warning: Don't use this tool with a calendar that is used for anything other than the support rota. The tool will delete all events from the specified start date onwards before creating new ones (this is so you don't have to worry about creating duplicate events). :warning: WARNING

If you haven't had your GPG key added to the repository, get someone who has to add it by following the guidance, [here](./.git-crypt/README.md).

Clone the repository to your desired directory and decrypt it by running:

```
git-crypt unlock
```

Activate a Python virtual environment (tested with 3.10.4) then run:

```
pip install -r requirements.txt
```

Update the `settings.py` file where there are three dictionaries containing:

- Google Calendar API connection settings.
  - There are three default calendar IDs, `dev-1`, `dev-2` and `prod`, update the `calendar` value to one of these.
- The support team which is made up of two groups and defined as those that are and aren't G7s.
  - Update the team if needed and select which group to start a cycle with.
- The start date and the number of cycles you want the calendar to run for.
  - It's not compulsory but if updating an existing calendar, you should set the start date to begin when the cycle switches from G7s to everyone else, or vice versa.
  - One cycle is the number of days equal to the total number of individuals in the support team.

Login credentials for the moj.data.engineering.dev@gmail.com account which has the Google Calendar API enabled are stored in LastPass. Have these ready for the next step.

`cd` into the `analytical_platform_support_rota/` directory and run:

```
python generate_rota.py
```

A browser window will open and you'll have to accept the access request, you will need to log in with the username and password if you haven't already done so.

- The dataengineering@digital.justice.gov.uk can be used to verify the login if needed.
- A session token gets created so you don't have to do this every time.

If you have modified the `support_team` dictionary in `settings.py` you should also add or remove the same team members email addresses from the Support Rota Google calendar by going to the 'Share with specific people` section in the calendar settings.

The Google Calendar for Teams Events Slack integration is used to post reminders of who is on support that day to the [#analytical_platform](https://mojdt.slack.com/archives/CBVUV2613) team's channel. The configuration can be found, [here](https://mojdt.slack.com/services/4654101349667).

See the [data engineering Confluence space](https://dsdmoj.atlassian.net/l/cp/hBVj3UsV) for more details about support.

## Licence

[MIT Licence](LICENCE.md)
