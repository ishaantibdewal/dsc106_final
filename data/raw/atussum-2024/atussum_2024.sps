* Edit the FILE statement to reference the data file on your computer.

GET DATA  /TYPE = TXT
 /FILE = 'C:\atussum_2024.dat'
 /DELCASE = LINE
 /DELIMITERS = ","
 /ARRANGEMENT = DELIMITED
 /FIRSTCASE = 2
 /IMPORTCASE = ALL
 /VARIABLES =
TUCASEID A14
TUFINLWGT F8
TRYHHCHILD F8
TEAGE F8
TESEX F8
PEEDUCA F8
PTDTRACE F8
PEHSPNON F8
GTMETSTA F8
TELFS F8
TEMJOT F8
TRDPFTPT F8
TESCHENR F8
TESCHLVL F8
TRSPPRES F8
TESPEMPNOT F8
TRERNWA F8
TRCHILDNUM F8
TRSPFTPT F8
TEHRUSLT F8
TUDIARYDAY F8
TRHOLIDAY F8
TRTEC F8
TRTHH F8
t010101  F8
t010102  F8
t010201  F8
t010299  F8
t010301  F8
t010399  F8
t010401  F8
t010501  F8
t019999  F8
t020101  F8
t020102  F8
t020103  F8
t020104  F8
t020199  F8
t020201  F8
t020202  F8
t020203  F8
t020301  F8
t020302  F8
t020303  F8
t020401  F8
t020402  F8
t020499  F8
t020501  F8
t020502  F8
t020599  F8
t020601  F8
t020602  F8
t020699  F8
t020701  F8
t020799  F8
t020801  F8
t020899  F8
t020901  F8
t020902  F8
t020903  F8
t020904  F8
t020905  F8
t020999  F8
t029999  F8
t030101  F8
t030102  F8
t030103  F8
t030104  F8
t030105  F8
t030106  F8
t030108  F8
t030109  F8
t030110  F8
t030111  F8
t030112  F8
t030199  F8
t030201  F8
t030202  F8
t030203  F8
t030299  F8
t030301  F8
t030302  F8
t030303  F8
t030399  F8
t030401  F8
t030402  F8
t030403  F8
t030404  F8
t030405  F8
t030499  F8
t030501  F8
t030502  F8
t030503  F8
t030504  F8
t030599  F8
t039999  F8
t040101  F8
t040102  F8
t040103  F8
t040104  F8
t040105  F8
t040106  F8
t040108  F8
t040109  F8
t040110  F8
t040111  F8
t040112  F8
t040199  F8
t040201  F8
t040203  F8
t040299  F8
t040301  F8
t040302  F8
t040303  F8
t040401  F8
t040402  F8
t040403  F8
t040404  F8
t040405  F8
t040499  F8
t040501  F8
t040502  F8
t040503  F8
t040504  F8
t040505  F8
t040506  F8
t040507  F8
t040508  F8
t040599  F8
t049999  F8
t050101  F8
t050102  F8
t050104  F8
t050199  F8
t050201  F8
t050202  F8
t050203  F8
t050205  F8
t050301  F8
t050302  F8
t050303  F8
t050304  F8
t050305  F8
t050399  F8
t050401  F8
t050403  F8
t059999  F8
t060101  F8
t060102  F8
t060103  F8
t060104  F8
t060199  F8
t060201  F8
t060202  F8
t060299  F8
t060301  F8
t060302  F8
t060399  F8
t060401  F8
t060402  F8
t060499  F8
t069999  F8
t070101  F8
t070102  F8
t070103  F8
t070104  F8
t070105  F8
t070199  F8
t070201  F8
t080101  F8
t080102  F8
t080201  F8
t080202  F8
t080203  F8
t080299  F8
t080301  F8
t080401  F8
t080402  F8
t080403  F8
t080499  F8
t080501  F8
t080502  F8
t080601  F8
t080701  F8
t080702  F8
t089999  F8
t090101  F8
t090102  F8
t090103  F8
t090199  F8
t090201  F8
t090202  F8
t090301  F8
t090302  F8
t090401  F8
t090402  F8
t090501  F8
t090502  F8
t090599  F8
t100102  F8
t100103  F8
t100199  F8
t100201  F8
t100299  F8
t100304  F8
t100305  F8
t110101  F8
t110201  F8
t120101  F8
t120201  F8
t120202  F8
t120299  F8
t120301  F8
t120302  F8
t120303  F8
t120304  F8
t120305  F8
t120306  F8
t120307  F8
t120308  F8
t120309  F8
t120310  F8
t120311  F8
t120312  F8
t120313  F8
t120399  F8
t120401  F8
t120402  F8
t120403  F8
t120404  F8
t120499  F8
t120501  F8
t120504  F8
t129999  F8
t130101  F8
t130102  F8
t130103  F8
t130104  F8
t130105  F8
t130106  F8
t130107  F8
t130108  F8
t130109  F8
t130110  F8
t130112  F8
t130113  F8
t130114  F8
t130116  F8
t130117  F8
t130118  F8
t130119  F8
t130120  F8
t130122  F8
t130124  F8
t130125  F8
t130126  F8
t130127  F8
t130128  F8
t130129  F8
t130130  F8
t130131  F8
t130132  F8
t130133  F8
t130134  F8
t130135  F8
t130136  F8
t130199  F8
t130202  F8
t130203  F8
t130204  F8
t130210  F8
t130213  F8
t130216  F8
t130218  F8
t130219  F8
t130222  F8
t130224  F8
t130225  F8
t130226  F8
t130227  F8
t130232  F8
t130299  F8
t130301  F8
t130302  F8
t140101  F8
t140102  F8
t140103  F8
t140105  F8
t150101  F8
t150102  F8
t150103  F8
t150104  F8
t150105  F8
t150106  F8
t150199  F8
t150201  F8
t150202  F8
t150203  F8
t150204  F8
t150299  F8
t150301  F8
t150302  F8
t150401  F8
t150402  F8
t150499  F8
t150501  F8
t150601  F8
t150602  F8
t150701  F8
t150801  F8
t150899  F8
t159999  F8
t160101  F8
t160102  F8
t160103  F8
t160104  F8
t160105  F8
t160106  F8
t160107  F8
t160108  F8
t160199  F8
t160201  F8
t180101  F8
t180201  F8
t180202  F8
t180203  F8
t180204  F8
t180205  F8
t180206  F8
t180207  F8
t180208  F8
t180209  F8
t180299  F8
t180301  F8
t180302  F8
t180303  F8
t180304  F8
t180305  F8
t180401  F8
t180402  F8
t180403  F8
t180404  F8
t180405  F8
t180499  F8
t180501  F8
t180502  F8
t180503  F8
t180504  F8
t180599  F8
t180601  F8
t180602  F8
t180603  F8
t180604  F8
t180699  F8
t180701  F8
t180702  F8
t180703  F8
t180704  F8
t180799  F8
t180801  F8
t180802  F8
t180803  F8
t180804  F8
t180805  F8
t180806  F8
t180807  F8
t180899  F8
t180901  F8
t180902  F8
t180903  F8
t180904  F8
t180905  F8
t181001  F8
t181002  F8
t181101  F8
t181201  F8
t181202  F8
t181203  F8
t181204  F8
t181205  F8
t181299  F8
t181301  F8
t181302  F8
t181399  F8
t181401  F8
t181501  F8
t181599  F8
t181601  F8
t181801  F8
t189999  F8
t500101  F8
t500103  F8
t500105  F8
t500106  F8
t500107  F8
t509999  F8
.
VARIABLE LABELS
label variable t010101 "Sleeping";
label variable t010102 "Sleeplessness";
label variable t010201 "Washing, dressing and grooming oneself";
label variable t010299 "Grooming, n.e.c.*";
label variable t010301 "Health-related self care";
label variable t010399 "Self care, n.e.c.*";
label variable t010401 "Personal/Private activities";
label variable t010501 "Personal emergencies";
label variable t019999 "Personal care, n.e.c.*";
label variable t020101 "Interior cleaning";
label variable t020102 "Laundry";
label variable t020103 "Sewing, repairing, and maintaining textiles";
label variable t020104 "Storing interior hh items, inc. food";
label variable t020199 "Housework, n.e.c.*";
label variable t020201 "Food and drink preparation";
label variable t020202 "Food presentation";
label variable t020203 "Kitchen and food clean-up";
label variable t020301 "Interior arrangement, decoration, and repairs";
label variable t020302 "Building and repairing furniture";
label variable t020303 "Heating and cooling";
label variable t020401 "Exterior cleaning";
label variable t020402 "Exterior repair, improvements, and decoration";
label variable t020499 "Exterior maintenance, repair and decoration, n.e.c.*";
label variable t020501 "Lawn, garden, and houseplant care";
label variable t020502 "Ponds, pools, and hot tubs";
label variable t020599 "Lawn and garden, n.e.c.*";
label variable t020601 "Care for animals and pets (not veterinary care)";
label variable t020602 "Walking / exercising / playing with animals";
label variable t020699 "Pet and animal care, n.e.c.*";
label variable t020701 "Vehicle repair and maintenance (by self)";
label variable t020799 "Vehicles, n.e.c.*";
label variable t020801 "Appliance, tool, and toy set-up, repair, and maintenance (by self)";
label variable t020899 "Appliances and tools, n.e.c.*";
label variable t020901 "Financial management";
label variable t020902 "Household and personal organization and planning";
label variable t020903 "HH and personal mail and messages (except e-mail)";
label variable t020904 "HH and personal e-mail and messages";
label variable t020905 "Home security";
label variable t020999 "Household management, n.e.c.*";
label variable t029999 "Household activities, n.e.c.*";
label variable t030101 "Physical care for hh children";
label variable t030102 "Reading to/with hh children";
label variable t030103 "Playing with hh children, not sports";
label variable t030104 "Arts and crafts with hh children";
label variable t030105 "Playing sports with hh children";
label variable t030106 "Talking with/listening to hh children";
label variable t030108 "Organization and planning for hh children";
label variable t030109 "Looking after hh children (as a primary activity)";
label variable t030110 "Attending hh children's events";
label variable t030111 "Waiting for/with hh children";
label variable t030112 "Picking up/dropping off hh children";
label variable t030199 "Caring for and helping hh children, n.e.c.*";
label variable t030201 "Homework (hh children)";
label variable t030202 "Meetings and school conferences (hh children)";
label variable t030203 "Home schooling of hh children";
label variable t030299 "Activities related to hh child's education, n.e.c.*";
label variable t030301 "Providing medical care to hh children";
label variable t030302 "Obtaining medical care for hh children";
label variable t030303 "Waiting associated with hh children's health";
label variable t030399 "Activities related to hh child's health, n.e.c.*";
label variable t030401 "Physical care for hh adults";
label variable t030402 "Looking after hh adult (as a primary activity)";
label variable t030403 "Providing medical care to hh adult";
label variable t030404 "Obtaining medical and care services for hh adult";
label variable t030405 "Waiting associated with caring for household adults";
label variable t030499 "Caring for household adults, n.e.c.*";
label variable t030501 "Helping hh adults";
label variable t030502 "Organization and planning for hh adults";
label variable t030503 "Picking up/dropping off hh adult";
label variable t030504 "Waiting associated with helping hh adults";
label variable t030599 "Helping household adults, n.e.c.*";
label variable t039999 "Caring for and helping hh members, n.e.c.*";
label variable t040101 "Physical care for nonhh children";
label variable t040102 "Reading to/with nonhh children";
label variable t040103 "Playing with nonhh children, not sports";
label variable t040104 "Arts and crafts with nonhh children";
label variable t040105 "Playing sports with nonhh children";
label variable t040106 "Talking with/listening to nonhh children";
label variable t040108 "Organization and planning for nonhh children";
label variable t040109 "Looking after nonhh children (as primary activity)";
label variable t040110 "Attending nonhh children's events";
label variable t040111 "Waiting for/with nonhh children";
label variable t040112 "Dropping off/picking up nonhh children";
label variable t040199 "Caring for and helping nonhh children, n.e.c.*";
label variable t040201 "Homework (nonhh children)";
label variable t040203 "Home schooling of nonhh children";
label variable t040299 "Activities related to nonhh child's educ., n.e.c.*";
label variable t040301 "Providing medical care to nonhh children";
label variable t040302 "Obtaining medical care for nonhh children";
label variable t040303 "Waiting associated with nonhh children's health";
label variable t040401 "Physical care for nonhh adults";
label variable t040402 "Looking after nonhh adult (as a primary activity)";
label variable t040403 "Providing medical care to nonhh adult";
label variable t040404 "Obtaining medical and care services for nonhh adult";
label variable t040405 "Waiting associated with caring for nonhh adults";
label variable t040499 "Caring for nonhh adults, n.e.c.*";
label variable t040501 "Housework, cooking, and shopping assistance for nonhh adults";
label variable t040502 "House and lawn maintenance and repair assistance for nonhh adults";
label variable t040503 "Animal and pet care assistance for nonhh adults";
label variable t040504 "Vehicle and appliance maintenance/repair assistance for nonhh adults";
label variable t040505 "Financial management assistance for nonhh adults";
label variable t040506 "Household management and paperwork assistance for nonhh adults";
label variable t040507 "Picking up/dropping off nonhh adult";
label variable t040508 "Waiting associated with helping nonhh adults";
label variable t040599 "Helping nonhh adults, n.e.c.*";
label variable t049999 "Caring for and helping nonhh members, n.e.c.*";
label variable t050101 "Work, main job";
label variable t050102 "Work, other job(s)";
label variable t050104 "Waiting associated with working";
label variable t050199 "Working, n.e.c.*";
label variable t050201 "Socializing, relaxing, and leisure as part of job";
label variable t050202 "Eating and drinking as part of job";
label variable t050203 "Sports and exercise as part of job";
label variable t050205 "Waiting associated with work-related activities";
label variable t050301 "Income-generating hobbies, crafts, and food";
label variable t050302 "Income-generating performances";
label variable t050303 "Income-generating services";
label variable t050304 "Income-generating rental property activities";
label variable t050305 "Waiting associated with other income-generating activities";
label variable t050399 "Other income-generating activities, n.e.c.*";
label variable t050401 "Job search activities";
label variable t050403 "Job interviewing";
label variable t059999 "Work and work-related activities, n.e.c.*";
label variable t060101 "Taking class for degree, certification, or licensure";
label variable t060102 "Taking class for personal interest";
label variable t060103 "Waiting associated with taking classes";
label variable t060104 "Security procedures rel. to taking classes";
label variable t060199 "Taking class, n.e.c.*";
label variable t060201 "Extracurricular club activities";
label variable t060202 "Extracurricular music and performance activities";
label variable t060299 "Education-related extracurricular activities, n.e.c.*";
label variable t060301 "Research/homework for class for degree, certification, or licensure";
label variable t060302 "Research/homework for class for pers. interest";
label variable t060399 "Research/homework n.e.c.*";
label variable t060401 "Administrative activities: class for degree, certification, or licensure";
label variable t060402 "Administrative activities: class for personal interest";
label variable t060499 "Administrative for education, n.e.c.*";
label variable t069999 "Education, n.e.c.*";
label variable t070101 "Grocery shopping";
label variable t070102 "Purchasing gas";
label variable t070103 "Purchasing food (not groceries)";
label variable t070104 "Shopping, except groceries, food and gas";
label variable t070105 "Waiting associated with shopping";
label variable t070199 "Shopping, n.e.c.*";
label variable t070201 "Comparison shopping";
label variable t080101 "Using paid childcare services";
label variable t080102 "Waiting associated w/purchasing childcare svcs";
label variable t080201 "Banking";
label variable t080202 "Using other financial services";
label variable t080203 "Waiting associated w/banking/financial services";
label variable t080299 "Using financial services and banking, n.e.c.*";
label variable t080301 "Using legal services";
label variable t080401 "Using health and care services outside the home";
label variable t080402 "Using in-home health and care services";
label variable t080403 "Waiting associated with medical services";
label variable t080499 "Using medical services, n.e.c.*";
label variable t080501 "Using personal care services";
label variable t080502 "Waiting associated w/personal care services";
label variable t080601 "Activities rel. to purchasing/selling real estate";
label variable t080701 "Using veterinary services";
label variable t080702 "Waiting associated with veterinary services";
label variable t089999 "Professional and personal services, n.e.c.*";
label variable t090101 "Using interior cleaning services";
label variable t090102 "Using meal preparation services";
label variable t090103 "Using clothing repair and cleaning services";
label variable t090199 "Using household services, n.e.c.*";
label variable t090201 "Using home maint/repair/décor/construction svcs";
label variable t090202 "Waiting associated w/ home main/repair/décor/constr";
label variable t090301 "Using pet services";
label variable t090302 "Waiting associated with pet services";
label variable t090401 "Using lawn and garden services";
label variable t090402 "Waiting associated with using lawn and garden services";
label variable t090501 "Using vehicle maintenance or repair services";
label variable t090502 "Waiting associated with vehicle main. or repair svcs";
label variable t090599 "Using vehicle maint. and repair svcs, n.e.c.*";
label variable t100102 "Using social services";
label variable t100103 "Obtaining licenses and paying fines, fees, taxes";
label variable t100199 "Using government services, n.e.c.*";
label variable t100201 "Civic obligations and participation";
label variable t100299 "Civic obligations and participation, n.e.c.*";
label variable t100304 "Waiting associated with using government services";
label variable t100305 "Waiting associated with civic obligations and participation";
label variable t110101 "Eating and drinking";
label variable t110201 "Waiting associated w/eating and drinking";
label variable t120101 "Socializing and communicating with others";
label variable t120201 "Attending or hosting parties/receptions/ceremonies";
label variable t120202 "Attending meetings for personal interest (not volunteering)";
label variable t120299 "Attending/hosting social events, n.e.c.*";
label variable t120301 "Relaxing, thinking";
label variable t120302 "Tobacco and drug use";
label variable t120303 "Television and movies (not religious)";
label variable t120304 "Television (religious)";
label variable t120305 "Listening to the radio";
label variable t120306 "Listening to/playing music (not radio)";
label variable t120307 "Playing games";
label variable t120308 "Computer use for leisure (exc. Games)";
label variable t120309 "Arts and crafts as a hobby";
label variable t120310 "Collecting as a hobby";
label variable t120311 "Hobbies, except arts and crafts and collecting";
label variable t120312 "Reading for personal interest";
label variable t120313 "Writing for personal interest";
label variable t120399 "Relaxing and leisure, n.e.c.*";
label variable t120401 "Attending performing arts";
label variable t120402 "Attending museums";
label variable t120403 "Attending movies/film";
label variable t120404 "Attending gambling establishments";
label variable t120499 "Arts and entertainment, n.e.c.*";
label variable t120501 "Waiting assoc. w/socializing and communicating";
label variable t120504 "Waiting associated with arts and entertainment";
label variable t129999 "Socializing, relaxing, and leisure, n.e.c.*";
label variable t130101 "Doing aerobics";
label variable t130102 "Playing baseball";
label variable t130103 "Playing basketball";
label variable t130104 "Biking";
label variable t130105 "Playing billiards";
label variable t130106 "Boating";
label variable t130107 "Bowling";
label variable t130108 "Climbing, spelunking, caving";
label variable t130109 "Dancing";
label variable t130110 "Participating in equestrian sports";
label variable t130112 "Fishing";
label variable t130113 "Playing football";
label variable t130114 "Golfing";
label variable t130116 "Hiking";
label variable t130117 "Playing hockey";
label variable t130118 "Hunting";
label variable t130119 "Participating in martial arts";
label variable t130120 "Playing racquet sports";
label variable t130122 "Rollerblading";
label variable t130124 "Running";
label variable t130125 "Skiing, ice skating, snowboarding";
label variable t130126 "Playing soccer";
label variable t130127 "Softball";
label variable t130128 "Using cardiovascular equipment";
label variable t130129 "Vehicle touring/racing";
label variable t130130 "Playing volleyball";
label variable t130131 "Walking";
label variable t130132 "Participating in water sports";
label variable t130133 "Weightlifting/strength training";
label variable t130134 "Working out, unspecified";
label variable t130135 "Wrestling";
label variable t130136 "Doing yoga";
label variable t130199 "Playing sports n.e.c.*";
label variable t130202 "Watching baseball";
label variable t130203 "Watching basketball";
label variable t130204 "Watching biking";
label variable t130210 "Watching equestrian sports";
label variable t130213 "Watching football";
label variable t130216 "Watching hockey";
label variable t130218 "Watching racquet sports";
label variable t130219 "Watching rodeo competitions";
label variable t130222 "Watching running";
label variable t130224 "Watching soccer";
label variable t130225 "Watching softball";
label variable t130226 "Watching vehicle touring/racing";
label variable t130227 "Watching volleyball";
label variable t130232 "Watching wrestling";
label variable t130299 "Attending sporting events, n.e.c.*";
label variable t130301 "Waiting related to playing sports or exercising";
label variable t130302 "Waiting related to attending sporting events";
label variable t140101 "Attending religious services";
label variable t140102 "Participation in religious practices";
label variable t140103 "Waiting associated w/religious and spiritual activities";
label variable t140105 "Religious education activities";
label variable t150101 "Computer use";
label variable t150102 "Organizing and preparing";
label variable t150103 "Reading";
label variable t150104 "Telephone calls (except hotline counseling)";
label variable t150105 "Writing";
label variable t150106 "Fundraising";
label variable t150199 "Administrative and support activities, n.e.c.*";
label variable t150201 "Food preparation, presentation, clean-up";
label variable t150202 "Collecting and delivering clothing and other goods";
label variable t150203 "Providing care";
label variable t150204 "Teaching, leading, counseling, mentoring";
label variable t150299 "Social service and care activities, n.e.c.*";
label variable t150301 "Building houses, wildlife sites, and other structures";
label variable t150302 "Indoor and outdoor maintenance, repair, and clean-up";
label variable t150401 "Performing";
label variable t150402 "Serving at volunteer events and cultural activities";
label variable t150499 "Participating in performance and cultural activities, n.e.c.*";
label variable t150501 "Attending meetings, conferences, and training";
label variable t150601 "Public health activities";
label variable t150602 "Public safety activities";
label variable t150701 "Waiting associated with volunteer activities";
label variable t150801 "Security procedures related to volunteer activities";
label variable t150899 "Security procedures related to volunteer activities, n.e.c.*";
label variable t159999 "Volunteer activities, n.e.c.*";
label variable t160101 "Telephone calls to/from family members";
label variable t160102 "Telephone calls to/from friends, neighbors, or acquaintances";
label variable t160103 "Telephone calls to/from education services providers";
label variable t160104 "Telephone calls to/from salespeople";
label variable t160105 "Telephone calls to/from professional or personal care svcs providers";
label variable t160106 "Telephone calls to/from household services providers";
label variable t160107 "Telephone calls to/from paid child or adult care providers";
label variable t160108 "Telephone calls to/from government officials";
label variable t160199 "Telephone calls (to or from), n.e.c.*";
label variable t160201 "Waiting associated with telephone calls";
label variable t180101 "Travel related to personal care";
label variable t180201 "Travel related to housework";
label variable t180202 "Travel related to food and drink prep., clean-up, and presentation";
label variable t180203 "Travel related to interior maintenance, repair, and decoration";
label variable t180204 "Travel related to exterior maintenance, repair, and decoration";
label variable t180205 "Travel related to lawn, garden, and houseplant care";
label variable t180206 "Travel related to care for animals and pets (not vet care)";
label variable t180207 "Travel related to vehicle care and maintenance (by self)";
label variable t180208 "Travel related to appliance, tool, and toy set-up, repair, and maintenance (by self)";
label variable t180209 "Travel related to household management";
label variable t180299 "Travel related to household activities, n.e.c.*";
label variable t180301 "Travel related to caring for and helping hh children";
label variable t180302 "Travel related to hh children's education";
label variable t180303 "Travel related to hh children's health";
label variable t180304 "Travel related to caring for hh adults";
label variable t180305 "Travel related to helping hh adults";
label variable t180401 "Travel related to caring for and helping nonhh children";
label variable t180402 "Travel related to nonhh children's education";
label variable t180403 "Travel related to nonhh children's health";
label variable t180404 "Travel related to caring for nonhh adults";
label variable t180405 "Travel related to helping nonhh adults";
label variable t180499 "Travel rel. to caring for and helping nonhh members, n.e.c.*";
label variable t180501 "Travel related to working";
label variable t180502 "Travel related to work-related activities";
label variable t180503 "Travel related to income-generating activities";
label variable t180504 "Travel related to job search and interviewing";
label variable t180599 "Travel related to work, n.e.c.*";
label variable t180601 "Travel related to taking class";
label variable t180602 "Travel related to extracurricular activities (ex. Sports)";
label variable t180603 "Travel related to research/homework";
label variable t180604 "Travel related to registration/administrative activities";
label variable t180699 "Travel related to education, n.e.c.*";
label variable t180701 "Travel related to grocery shopping";
label variable t180702 "Travel related to purchasing gas";
label variable t180703 "Travel related to purchasing food (not groceries)";
label variable t180704 "Travel related to shopping, ex groceries, food, and gas";
label variable t180799 "Travel related to consumer purchases, n.e.c.*";
label variable t180801 "Travel related to using childcare services";
label variable t180802 "Travel related to using financial services and banking";
label variable t180803 "Travel related to using legal services";
label variable t180804 "Travel related to using medical services";
label variable t180805 "Travel related to using personal care services";
label variable t180806 "Travel related to using real estate services";
label variable t180807 "Travel related to using veterinary services";
label variable t180899 "Travel rel. to using prof. and personal care services, n.e.c.*";
label variable t180901 "Travel related to using household services";
label variable t180902 "Travel related to using home main./repair/décor./construction svcs";
label variable t180903 "Travel related to using pet services (not vet)";
label variable t180904 "Travel related to using lawn and garden services";
label variable t180905 "Travel related to using vehicle maintenance and repair services";
label variable t181001 "Travel related to using government services";
label variable t181002 "Travel related to civic obligations and participation";
label variable t181101 "Travel related to eating and drinking";
label variable t181201 "Travel related to socializing and communicating";
label variable t181202 "Travel related to attending or hosting social events";
label variable t181203 "Travel related to relaxing and leisure";
label variable t181204 "Travel related to arts and entertainment";
label variable t181205 "Travel as a form of entertainment";
label variable t181299 "Travel rel. to socializing, relaxing, and leisure, n.e.c.*";
label variable t181301 "Travel related to participating in sports/exercise/recreation";
label variable t181302 "Travel related to attending sporting/recreational events";
label variable t181399 "Travel related to sports, exercise, and recreation, n.e.c.*";
label variable t181401 "Travel related to religious/spiritual practices";
label variable t181501 "Travel related to volunteering";
label variable t181599 "Travel related to volunteer activities, n.e.c.*";
label variable t181601 "Travel related to phone calls";
label variable t181801 "Security procedures related to traveling";
label variable t189999 "Traveling, n.e.c.*";
label variable t500101 "Insufficient detail in verbatim";
label variable t500103 "Missing travel or destination";
label variable t500105 "Respondent refused to provide information/'none of your business'";
label variable t500106 "Gap/can't remember";
label variable t500107 "Unable to code activity at 1st tier";
label variable t509999 "Data codes, n.e.c.*";
.

VALUE LABELS
GTMETSTA
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Metropolitan"
2 "Non-metropolitan"
3 "Not identified"
/
PEEDUCA
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
31 "Less than 1st grade"
32 "1st, 2nd, 3rd, or 4th grade"
33 "5th or 6th grade"
34 "7th or 8th grade"
35 "9th grade"
36 "10th grade"
37 "11th grade"
38 "12th grade - no diploma"
39 "High school graduate - diploma or equivalent [GED]"
40 "Some college but no degree"
41 "Associate degree - occupational-vocational"
42 "Associate degree - academic program"
43 "Bachelor's degree [BA, AB, BS, etc.]"
44 "Master's degree [MA, MS, MEng, MEd, MSW, etc.]"
45 "Professional school degree [MD, DDS, DVM, etc.]"
46 "Doctoral degree [PhD, EdD, etc.]"
/
PEHSPNON
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Hispanic"
2 "Non-Hispanic"
/
PTDTRACE
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "White only"
2 "Black only"
3 "American Indian, Alaskan Native only"
4 "Asian only"
5 "Hawaiian-Pacific Islander only"
6 "White-Black"
7 "White-American Indian"
8 "White-Asian"
9 "White-Hawaiian"
10 "Black-American Indian"
11 "Black-Asian"
12 "Black-Hawaiian"
13 "American Indian-Asian"
14 "American Indian-Hawaiian"
15 "Asian-Hawaiian"
16 "White-Black-American Indian"
17 "White-Black-Asian"
18 "White-Black-Hawaiian"
19 "White-American Indian-Asian"
20 "White-American Indian-Hawaiian"
21 "White-Asian-Hawaiian"
22 "Black-American Indian-Asian"
23 "White-Black-American Indian-Asian"
24 "White-American Indian-Asian-Hawaiian"
25 "Other 3 race combinations"
26 "Other 4 and 5 race combinations"
/
TELFS
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Employed - at work"
2 "Employed - absent"
3 "Unemployed - on layoff"
4 "Unemployed - looking"
5 "Not in labor force"
/
TEMJOT
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Yes"
2 "No"
/
TESCHENR
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Yes"
2 "No"
/
TESCHLVL
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "High school"
2 "College or university"
/
TESEX
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Male"
2 "Female"
/
TESPEMPNOT
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Employed"
2 "Not employed"
/
TRDPFTPT
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Full time"
2 "Part time"
/
TRSPFTPT
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Full time"
2 "Part time"
3 "Hours vary"
/
TRSPPRES
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Spouse present"
2 "Unmarried partner present"
3 "No spouse or unmarried partner present"
/
TRHOLIDAY
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
0 "Diary day was not a holiday"
1 "Diary day was a holiday"
/
TUDIARYDAY
-1 "Blank"
-2 "Don't Know"
-3 "Refused"
1 "Sunday"
2 "Monday"
3 "Tuesday"
4 "Wednesday"
5 "Thursday"
6 "Friday"
7 "Saturday"
/
.
CACHE.
EXECUTE.
