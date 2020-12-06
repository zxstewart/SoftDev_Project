### Start of David Dayan Commits:
* f253a97 Update contributions.md
* 2983756 Update contributions.md
* d78462a Rename contributions.txt to contributions.md
* b1a4426 added list of git contributions by member from git log
* 5bc04db Update README.md
* 4a07153 Delete ProjectMileston6_203_4.pdf
* f9ec9cb Add files via upload
* 20d916b Merge branch 'master' of github.com:CSCI-3308-CU-Boulder/203_4_F20
* 4496e8d listing players in favorite player add and download data by player alphabetically
* 903b38d fixed issue with incorrect team name from abbreviation
* cba2344 Merge branch 'master' of github.com:CSCI-3308-CU-Boulder/203_4_F20
* 033fb41 working favorite player add feature for all sports: fixed control issue
* ba2e172 added support for team name field in favorite player
* b1df1b7 Merge branch 'master' of github.com:CSCI-3308-CU-Boulder/203_4_F20
* a07baa1 fixed sport type for favorite players
* 9619367 Merge branch 'master' of github.com:CSCI-3308-CU-Boulder/203_4_F20
* 9e1ad15 formatted and added more player-specific info for favorite players
* 871cfda making favorite player page and account page more readable
* a1f081a adding favorite players working for nfl players
* b24de6c updated database loading
* e422c31 Merge branch 'master' of github.com:CSCI-3308-CU-Boulder/203_4_F20
* b6ea898 fixing favorite player database object and compare page
* bcec769 fixed merge conflict reverting to old database
* b22c031 added more fields for favorite player db model, adjusted chart function
* 0a6109f changed favorite player addition to dynamic selection
* 730847d added route for getting all possible teams that Favorite player has played
* cd7d929 added route for fetching JSON of players for favorite players
* e7a7b1e change favorite players form to selectfield and reordered form order
* c6bb5e5 Merge branch 'master' of github.com:CSCI-3308-CU-Boulder/203_4_F20
* ced1bea added to download data function for players
* 8de1027 return json of players from getplayers route
* 36b5ed8 expanded league-wide download to nhl, mlb, and nba
* 709bdca fixed broken dynamic team field
* e94b408 working league stats download for NFL
* c95c7f7 added js to fix some form issues with download data
* 4d0c842 fixed issue with Favorite Database table in account route
* 37103b8 deleted old csv files: wiping database
* 6e7bda9 fixed conflict in database
* a31570c view csv as table feature and additional debugging fixes
* 4279702 removed helper function, fixed form toggle for different data download type
* e0c8587 removed redundant team abbreviation check since dropdown selection is implemented
* 7d03757 completed dynamic form dropdown based on sports and year
* a9497f7 added routes for querying DB to get teams and team abbreviations for dropdown
* 884e602 Merge branch 'master' of github.com:CSCI-3308-CU-Boulder/203_4_F20
* 6edd270 added code for loading database with teams used in dynamic dropdown
* f791799 different home pages for logged in and non-authenticated users
* e7e9f4e checking verification of my commit
* a8db6b9 fixed download data button to work with all possible app routes
* 42989fe Merge branch 'master' of github.com:CSCI-3308-CU-Boulder/203_4_F20
* 359d117 display the previously downloaded files of user: allow user to redownload files as well
* 83b5d4d dynamic home page to display previous downloaded files
* 43bdb4d add downloaded data object to database associated with user
* 97e2898 fixed interests DB field, added feature for associating downloaded data csv to user in database
* a53d40d removed profile.html depracated page
* 661626e fixed bug with account update: email verification
* f7dea66 removed register.html, updated form registration. Also added file for helper function etc
* 98fc301 Add files via upload
* 7a4d0cc added team abbreviation validation for download data form
* efde25b solved imported libraries merge conflict
* e24d74e added download schedule stats for all available professional sports
* d39e1c9 completed download data by team for NFL
* 70fb77b Add files via upload
* 8c5967f fixed validation for season year and team abbreviation fields in download data
* b5c1f9d implemented download data template to accept form and post
* c04a5aa added form routing and definition for downloadData feature
* a533d38 begin implementation of download data feature
* f43bd59 user can login then redirect back to page that required login
* 5fb8e7f updated account page: now only accessible while logged in
* 3f4a306 added logout and dynamic nav bar functionality
* 1fd2c17 updated login to check users from database
* f60fa95 updated dependencies list
* 2140b96 updated registration forms backend to prevent accounts with same username/email from being created and added to db
* 54f839e updated user registration to add users to database
* 32f4be3 updated registration to add user info to database
* a9fb5f8 updated structure to handle app as package: USE runsportsApp.py instead of sportsApp.py to run application
* d5cd275 updated basic forms for database
* cac476e updated routing for navbar in layout template
* e6001bd updated routes for login page
* 089d589 updated login page to work with boostrap and flask POST
* e745f1d update register page to accept GET and POST requests
* 8a40c87 updated routing and added file to indicate dependency files
* 61ca7c3 Pushed Project Milestone 3
* 5f6d1a6 Delete README.md
* 16298fb fixed register page: now working!
* df0f30e added images and routing for images of sports from static folder
* 0d2cf06 updated routing for register page, fixed locally hosted images (they now show up)
* a1ea583 updated css for card images and added images to browse page
* 7cf0ed2 added images for NFL
* 3a09f43 added routing to browse.html in flask backend
* 26ee287 verified that ssh key is working
* 9169dd9 testing if my ssh for github works
* 775365d updated browse page search and sport slection to work with layout.html
* a371986 added intermediate file to reorganize browse.html to work with templates
* 08763ec additional test data gathering from API
* 9416654 Update README.md
* 72b5bde Update README.md
* 8852998 Update README.md
* f295e3a removed local Package Lock files
* 1eac21a added new testing
* c33bc10 updated readme with instructions for how to install sportsreference package
* e0c1c46 removed redundant script for running site
* 5910338 updated packages and testing dynamic visualizations
* c79ea5d Update README.md
* bed8467 updated README with instructions to run site locally
* 0a79e1b added more style with Boostrap and pages, navbar
* 775915e created static folder to hold JS and CSS files
* 80b2a35 added boostrap support to layout.html that adds Bootstrap functionality to all html files
* ebd8571 adding templates to support passing python info from DB
* 16ba9b5 Testing Sports-reference api
* 9544cd5 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 Merging to get index.html in
* 7b747d3 added index.html
* f853fcf created basic routs between pages in flask python file
* 4455882 first flask application and script to run
* ce89b88 formatting
* c2b842d formatting
* a9bff5b completed documentation for installing pipenv
* 7cb1548 updated instructions for installing pipenv
* b7ac019 updated README for pipenv
* 9b4ade5 more documentation
* 23da203 added contributors
* 7b41061 updated README.md
* 3c0313e updated README with instructions on how to set up virtual python environments
* 98071f9 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 Deleted django project, switching to flask project due to project constraints
* 011efd2 deleted django project switching to flask
* 3406636 Update README.md
* cb17444 Merge pull request #5 from CSCI-3308-CU-Boulder/makayla
* f2219cf added home landing functions in views.py
* 5ad37a7 created sportsApp
* 674a048 created runlocal.sh script to be used to run the local host website
* 8f8bf5a created sports_stats_master django project
* 8146052 updated README.md with basic description
* 85aae4a Deleted redundant ReadMe.md file
* cd57a65 Merge pull request #4 from CSCI-3308-CU-Boulder/zoe
* 3576d68 Merge branch 'master' into zoe
* 6b16022 Merge pull request #2 from CSCI-3308-CU-Boulder/Mitch_Branch
* c4a7a4e Merge branch 'master' into Mitch_Branch
* 47f3a9b Updated README
* 46ae04f made changes by adding header on branch David
* 8ce770b Added name David Dayan
* dd32ab6 Create README.md

------------------------------------------

### Start of Zoe Stewart Commits:
* b0731b7 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* d268598 got rid of update player button
* 6914a80 fixed add favorite redirect
* 8fe76dd Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* b1c31f1 separate favorites page
* 2e1d823 video page styling
* c53ae07 fPlayer styling
* 491b735 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* c1a7bff nothing useful, fixing github problem
* 3eaca4b fixing merge problem i think
* f98054b Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* b5c0467 can delete players from favorites
* 1494a3f add to favorite works now
* 09122f1 added favorite page, db part not yet
* ccc36f1 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* 99e9302 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* 1e9f508 hopefully adding to my branch
* c742146 just made the profile image round w shadow
* 375a696 forgot to update route for settings page
* 02e53cf added settings page, edited some formatting:
* 6986594 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* f20ed5a layout changes
* 23300df fixed some video styling, card columns don't work idk
* 28a76e1 account page viewable, modifications not quite
* a9c5223 fixed embed on video page and changed layout
* e1d77e6 more account updates
* c3f9c90 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 merge to pull updates
* 610604a updating account page
* 9ec47fa Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 updating stuff
* e770d09 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 merging to pull, idk why i have to keep doing this
* 543346f Merge branch 'master' of https:* //github.com/CSCI-3308-CU-Boulder/203_4_F20 merging to pull new stuff
* 7bcf617 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* bfa6c2b have to commit before i can pull i guess
* 63137c4 fixed some video formatting
* 5e17f1d added a rough video page
* 3444196 added profile page, connected search
* 3fffb19 fixed layout integration, still need to include flask link
* c5aa957 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 idk had to merge again...
* 4315235 fixed layout integration for browse and registration form
* 4ec6726 Merge https://github.com/CSCI-3308-CU-Boulder/203_4_F20 um merging because i had to pull before letting me push changes?
* a6a8560 browse page outline?
* 9bd8462 edited README
* 7939676 adding README.md?
* 9c03a32 um adding ReadMe.md and names
* 90d660a Added name Zoe Stewart

------------------------------------------

### Start of Quinn Stone Commits:
* cfe9a26 Update baseball.html
* 887ce53 Update soccer.html
* 00acfa9 Update basketball.html
* 1c18195 Update football.html
* f10e018 Update hockey.html
* b76d369 Update basketball.html
* 0ce080b Update basketball.html
* a8f6366 Update football.html
* dc3c2ee Update htmltable.py
* a0bbc55 Centered text
* 74e5237 Centered text
* c1f7a0a Update football.html
* d6cf426 Centered text
* 244704f Centered text
* f1b5ac6 Update routes.py
* 596b27e Update browse.html
* f090bdd Create other.html
* 9c07c53 Update htmltable.py
* 45a55a3 Update htmltable.py
* 59ed889 Create htmltable.py
* 35ac992 Create db_helper.py
* 4b003ed Update hockey.html
* 6bf5e4f Update basketball.html
* 0043201 Update hockey.html
* 401adf8 Update soccer.html
* 638b7e0 Update hockey.html
* 8722c21 Update football.html
* a8e0e57 Update baseball.html
* 4161f71 Update about.html
* d13d384 Update baseball.html
* 62e5c9a Add files via upload
* 95a6b0b Update browse.html
* 639fcbb Update sportsApp.py
* 8bec23f Update sportsApp.py
* 5dfbdc0 Update sportsApp.py
* 1e44712 Add files via upload
* 3c19a61 I added my name
* cab41d5 I added my name
* a54e51b I added my name
* 6cfd91a Update README.md
* 08d9d68 Update README.md

------------------------------------------

### Start of John Lee Commits:
* 4f720bf merge
* eae2d08 check invalid player and regex form
* 7749e09 added graph and table to favorite player
* af656f7 added table to compare
* 58783c0 finishing  up graphs
* 6d2a9c7 chartjs multiple graphs
* 4736f92 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 into master
* ff87090 minor compare changes
* 3aa4cdd compare changes
* f321554 ran into chart.js problems
* 24a22fc compare
* 5a57b12 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 into master
* d7bdc2c commit for pull
* bc54e26 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 into master
* 744e5d2 commit compare
* 4e645e4 small changes
* f100893 minor changes to compare function
* ec8fdb8 Made python function to get data from API
* 8080719 added sample bar graph to compare
* fc1d952 trying to fix compare errors
* 3b49cf5 updates to compare
* 20e57ea compare.html update
* b2da2c2 add compare link to layout sidebar
* 7b91294 minor compare fixes
* d457d40 adding compare route
* 48bb26e new register
* 69bcee8 minor changes
* 9382766 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 into master
* 4f99c8e undo changes
* 07d0f4d added forms.py, no frontend yet
* 166de1a Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 into master
* 158312b merging with local
* 106b50f Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20 into master
* 4956147 Update navbar links
* 6a10d02 Added About page
* ff4b300 Add files via upload
* 0e1bc34 Lab4 3.9
* 90405ea Lab4 3.6
* d0129b2 Lab4 3.4

------------------------------------------

### Start of Makayla Johnson Commits:
* 0599e1e Add files via upload
* 8a84e1e adding live stream
* ea3188a adding styling
* 229998f adding links to sports pages
* 30cf4f0 Update layout.html
* fe7677c Add files via upload
* ac26e96 Merge pull request #3 from CSCI-3308-CU-Boulder/John
* e8bd149 Merge branch 'master' into John
* 17bd492 message
* 74dd65d message

------------------------------------------

### Start of Mitch Lacroque Commits:
* 9055c44 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* 380dbbf Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* 95aec9c more attempts
* 996f7cf More procfile attempts
* fe69a42 more changes
* 2a35f2e Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* 0e03433 Procfile attempts
* 4380973 Heroku Gunicorn addition
* 16b7241 Merge branch 'master' of https://github.com/CSCI-3308-CU-Boulder/203_4_F20
* 56248f9 more testing
* a068cae heroku hosting attempts
* fb3bc35 Changed Compare Graph to prepare for Sports Reference API calls
* f0fe8fb Attempting to fix db errors
* 6730260 Merge pull request #6 from CSCI-3308-CU-Boulder/quinn
* fa2c7c5 Mitch's Branch
* 14ca0d9 updated README
* 75ca144 Create README.md
* 832ceb2 Create README.md
* 8434c2d Create README.md
