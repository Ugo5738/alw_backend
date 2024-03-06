from django.urls import path
from rest_framework.routers import DefaultRouter

from meetings import views

urlpatterns = []
router = DefaultRouter()

urlpatterns = [
    # meetings
    path("meetings-list/", views.MeetingListView.as_view(), name="meeting_list"),
    path(
        "meeting-event/<int:pk>/",
        views.MeetingDetailView.as_view(),
        name="meeting_detail",
    ),
]

# [
#     {
#         "id":2,
#         "title":"Blue note could.",
#         "scheduled_time":"2024-01-27T02:03:28Z",
#         "duration":145,
#         "agenda":"Her could give development another. Management quality fine western.\nThink day rest social. Identify buy network week develop.\nCultural pass his yard range.",
#         "notes":"So home PM participant pressure site. Poor people realize believe any hotel. Rock happen your woman fact.",
#         "outcomes":"Us kind never. Environmental ability prevent table north. No energy scientist.",
#         "location":"01783 Ronald Key\nTimothyfort, NH 27751",
#         "created_at":"2023-12-31T10:28:02.425201Z",
#         "created_by":{
#             "id":120,
#             "first_name":"Jennifer",
#             "last_name":"Camacho",
#             "email":"jennifer.camacho20231231102802303201@example.com",
#             "profile_picture":null
#         },
#         "participants":[]
#     },
#     {
#         "id":3,
#         "title":"Return cell.",
#         "scheduled_time":"2024-01-24T14:06:25Z",
#         "duration":67,
#         "agenda":"But go court parent would her right else. Fly of each particularly each.\nHundred east join manage public population. Foreign media leader this ask detail Mrs true.",
#         "notes":"Floor protect meeting receive attorney threat. Early suggest store later large skill pass.\nEconomy expect wish newspaper knowledge base talk. Risk necessary seem action.",
#         "outcomes":"Give through war marriage to price parent. Ever whose friend whatever watch simply science. Nature them child.\nActually eye seven short significant media. His explain certain lawyer model culture.",
#         "location":"442 Kevin Estate Apt. 628\nKimberlyport, AR 87060",
#         "created_at":"2023-12-31T10:28:03.085963Z",
#         "created_by":{
#             "id":122,
#             "first_name":"Susan",
#             "last_name":"Carter",
#             "email":"susan.carter20231231102802947591@example.com",
#             "profile_picture":null
#         },
#         "participants":[]
#     },
#     {   "id":6,
#         "title":"Chance remember impact.",
#         "scheduled_time":"2024-01-21T13:32:31Z",
#         "duration":112,
#         "agenda":"Value risk commercial group. Charge theory main president. Short on born score.\nTree sea identify wall at growth. Choose happy check hand ask lawyer crime.",
#         "notes":"Note yourself over type. Wife financial relationship on.\nCold system north city. Finish radio player me college small whom imagine.",
#         "outcomes":"Live rather their break analysis. Style account same worker. Focus occur on name.\nEnter also once management. Commercial prepare husband plan development return machine.",
#         "location":"8701 Nicole Parkway\nWest Audrey, AZ 92505",
#         "created_at":"2023-12-31T10:28:05.998561Z",
#         "created_by":{
#             "id":128,
#             "first_name":"Robin",
#             "last_name":"Phillips",
#             "email":"robin.phillips20231231102805800230@example.com",
#             "profile_picture":null
#         },
#         "participants":[]
#     },
#     {
#         "id":10,
#         "title":"Purpose often under.",
#         "scheduled_time":"2024-01-20T15:43:38Z",
#         "duration":127,
#         "agenda":"Here performance husband crime full at. Apply so floor bill safe. Agency occur fight condition rock role community.",
#         "notes":"Him officer beautiful arm. Rule become son interview low if.\nApproach always authority western. Take foot race but land.\nEnergy term behavior. Smile open race wife imagine send appear.",
#         "outcomes":"Edge list plan health that step. Us second despite beyond. Fly brother knowledge ability support rule.",
#         "location":"220 Parker Branch\nLake Patricia, AL 68922",
#         "created_at":"2023-12-31T10:28:10.433656Z",
#         "created_by":{"id":136,
#         "first_name":"Steven",
#         "last_name":"King",
#         "email":"steven.king20231231102810008340@example.com",
#         "profile_picture":null},
#         "participants":[]},{"id":5,
#         "title":"Small coach customer fact.",
#         "scheduled_time":"2024-01-19T13:08:19Z",
#         "duration":98,
#         "agenda":"Will buy choice then. Car health have ground them stage. Almost pull detail.\nSay thus leader simply. Have trial newspaper couple. Join represent cold win treat friend.",
#         "notes":"Politics fast from class pick. Treat indeed usually people authority conference prevent.",
#         "outcomes":"Us national oil partner article itself during. Cut someone statement.",
#         "location":"221 Michelle Spurs Suite 876\nNorth Jenniferfurt, ME 37083",
#         "created_at":"2023-12-31T10:28:05.099359Z",
#         "created_by":{"id":126,
#         "first_name":"Sherry",
#         "last_name":"Carter",
#         "email":"sherry.carter20231231102804892755@example.com","profile_picture":null},"participants":[]},{"id":1,"title":"Inside research.","scheduled_time":"2024-01-19T12:14:56Z","duration":100,"agenda":"Just clear sometimes including knowledge. Probably stuff down require mind thought.","notes":"Your less company soon. Certain interview who long truth.\nFuture now stand traditional southern. Few possible eat. Black wrong pattern computer.\nIssue gas card first.","outcomes":"Ok threat capital Mr simply daughter consider. Far interview oil drive mission everybody. Democrat game dinner store this imagine until my.","location":"17844 Allen Alley Apt. 439\nPort Lisa, PR 66829","created_at":"2023-12-31T10:28:01.797700Z","created_by":{"id":118,"first_name":"Kimberly","last_name":"Woods","email":"kimberly.woods20231231102801676813@example.com","profile_picture":null},"participants":[]},{"id":4,"title":"Hope trial.","scheduled_time":"2024-01-12T07:27:50Z","duration":176,"agenda":"Professional institution street. Color write capital data industry.\nHot oil change change television. This way whatever school four between. Recently science protect practice we property first PM.","notes":"Up oil model themselves program they possible. Tree listen quite field ever share. Meeting end letter amount world take.","outcomes":"Citizen yet prove office. Board gas college black sit skill draw.\nAdmit get particular. Decide film end matter. Blue century book identify. Black against mind mention wonder.","location":"PSC 7735, Box 7963\nAPO AA 76689","created_at":"2023-12-31T10:28:04.093701Z","created_by":{"id":124,"first_name":"Joyce","last_name":"Wilson","email":"joyce.wilson20231231102803919054@example.com","profile_picture":null},"participants":[]},{"id":8,"title":"Attack all language.","scheduled_time":"2024-01-07T11:34:37Z","duration":31,"agenda":"Still story involve cultural today thought star. Defense sister strong personal during base meeting. Moment like his finally individual.","notes":"Finish you similar series right minute. Bring set how possible office customer. Sing operation treatment form. Including store national friend discover.","outcomes":"Government walk citizen write other. Result author north support available.\nMaintain level chance forget possible south worker. Nice seek resource go kind.","location":"474 Freeman Avenue Apt. 903\nJohnchester, IA 23977","created_at":"2023-12-31T10:28:07.830734Z","created_by":{"id":132,"first_name":"Michelle","last_name":"Wood","email":"michelle.wood20231231102807570219@example.com","profile_picture":null},"participants":[]},{"id":9,"title":"Only practice sister.","scheduled_time":"2024-01-06T23:48:28Z","duration":134,"agenda":"Gun suggest strategy table some good necessary. Me some big letter black. Successful boy that culture why boy weight.\nSpace various specific particularly.","notes":"Red course manager hand really short money. Real range also tree treat remain popular. Rather throughout peace.\nFish like part crime huge. Agent rise heart.","outcomes":"Alone not pick recognize. Beat wall vote music whom.\nAgent produce simple. Your method short.\nLate them marriage government could growth.","location":"8980 Lori Ridges\nPatrickview, MI 10868","created_at":"2023-12-31T10:28:09.097508Z","created_by":{"id":134,"first_name":"Vanessa","last_name":"Morales","email":"vanessa.morales20231231102808787960@example.com","profile_picture":null},"participants":[]},{"id":7,"title":"Week practice challenge.","scheduled_time":"2024-01-05T12:00:45Z","duration":136,"agenda":"Central mention staff cut can. Physical effect role picture movie mention under. Indeed opportunity financial morning.\nSubject will they. His place then treatment question. Radio spring move long.","notes":"Lawyer understand rule interesting establish. Win interest reason. Any increase again read hour. Use guy score.\nAssume home born eight much population contain. Specific yard model among read back.","outcomes":"Letter career get safe year. For some break ask.\nAffect central two. Citizen manager light another agent fight.\nShe most writer. Difference dog half together safe peace size.","location":"834 King Radial\nCrystalstad, HI 83606","created_at":"2023-12-31T10:28:06.888667Z","created_by":{"id":130,"first_name":"Crystal","last_name":"Gibson","email":"crystal.gibson20231231102806733337@example.com","profile_picture":null},"participants":[]}]
