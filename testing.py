import re

# Paste your full printout text as a multi-line string:
data = """
0 American Sign Language: #/programs/SyJdy08nv?bc=true&bcCurrent=American%20Sign%20Language&bcItemType=programs
1 Anthropology: #/programs/BkG9aQ0GE?bc=true&bcCurrent=Anthropology&bcItemType=programs
2 Anthropology: #/programs/Sy2vaQAME?bc=true&bcCurrent=Anthropology&bcItemType=programs
3 Anthropology: #/programs/SyjvTmCzN?bc=true&bcCurrent=Anthropology&bcItemType=programs
4 Anthropology: #/programs/rJiDpQCGV?bc=true&bcCurrent=Anthropology&bcItemType=programs
5 Anthropology: #/programs/ry9wpXCfV?bc=true&bcCurrent=Anthropology&bcItemType=programs
6 Applications of Psychology and Leadership: #/programs/By-TC-EDj?bc=true&bcCurrent=Applications%20of%20Psychology%20and%20Leadership&bcItemType=programs
7 Applied Ethics: #/programs/rk6KpQRz4?bc=true&bcCurrent=Applied%20Ethics&bcItemType=programs
8 Applied Linguistics: #/programs/BJZUaX0fV?bc=true&bcCurrent=Applied%20Linguistics&bcItemType=programs
9 Applied Linguistics: #/programs/SJWIT7RMN?bc=true&bcCurrent=Applied%20Linguistics&bcItemType=programs
10 Applied Linguistics: #/programs/r1__TXCfN?bc=true&bcCurrent=Applied%20Linguistics&bcItemType=programs
11 Art Education: #/programs/SkeCp70fE?bc=true&bcCurrent=Art%20Education&bcItemType=programs
12 Art History and Visual Studies: #/programs/H1qNa7CzV?bc=true&bcCurrent=Art%20History%20and%20Visual%20Studies&bcItemType=programs
13 Art History and Visual Studies: #/programs/HJZK6mRGN?bc=true&bcCurrent=Art%20History%20and%20Visual%20Studies&bcItemType=programs
14 Art History and Visual Studies: #/programs/SJq46QAM4?bc=true&bcCurrent=Art%20History%20and%20Visual%20Studies&bcItemType=programs
15 Astronomy: #/programs/BkYvaXRMN?bc=true&bcCurrent=Astronomy&bcItemType=programs
16 Astronomy: #/programs/By-qaQRfE?bc=true&bcCurrent=Astronomy&bcItemType=programs
17 Astronomy: #/programs/r1lKPTXCz4?bc=true&bcCurrent=Astronomy&bcItemType=programs
18 Biochemistry: #/programs/HyaYpQ0f4?bc=true&bcCurrent=Biochemistry&bcItemType=programs
19 Biochemistry: #/programs/S1OI6mAfE?bc=true&bcCurrent=Biochemistry&bcItemType=programs
20 Biochemistry: #/programs/rkOUTXAME?bc=true&bcCurrent=Biochemistry&bcItemType=programs
21 Biochemistry and Chemistry: #/programs/SJNsoJXWt?bc=true&bcCurrent=Biochemistry%20and%20Chemistry&bcItemType=programs
22 Biochemistry and Chemistry: #/programs/Syg_IpQCfN?bc=true&bcCurrent=Biochemistry%20and%20Chemistry&bcItemType=programs
23 Biology: #/programs/BkYUaQCf4?bc=true&bcCurrent=Biology&bcItemType=programs
24 Biology: #/programs/S1gtLTm0ME?bc=true&bcCurrent=Biology&bcItemType=programs
25 Biology and Earth Sciences: #/programs/S1qLaQCf4?bc=true&bcCurrent=Biology%20and%20Earth%20Sciences&bcItemType=programs
26 Biology and Earth Sciences: #/programs/S1qLpX0MV?bc=true&bcCurrent=Biology%20and%20Earth%20Sciences&bcItemType=programs
27 Biology and Mathematics and Statistics: #/programs/B1gcL6X0fN?bc=true&bcCurrent=Biology%20and%20Mathematics%20and%20Statistics&bcItemType=programs
28 Biology and Psychology: #/programs/BJ9IpX0M4?bc=true&bcCurrent=Biology%20and%20Psychology&bcItemType=programs
29 Biology and Psychology: #/programs/HkjLT7RMV?bc=true&bcCurrent=Biology%20and%20Psychology&bcItemType=programs
30 Biology BA: #/programs/SyRtT7RGN?bc=true&bcCurrent=Biology%20BA&bcItemType=programs
31 Biology BSc: #/programs/HkCK67AGV?bc=true&bcCurrent=Biology%20BSc&bcItemType=programs
32 Biomedical Engineering: #/programs/ryO4TXRfV?bc=true&bcCurrent=Biomedical%20Engineering&bcItemType=programs
33 Business: #/programs/rJRup7RM4?bc=true&bcCurrent=Business&bcItemType=programs
34 Canadian Studies: #/programs/BJehdTmCf4?bc=true&bcCurrent=Canadian%20Studies&bcItemType=programs
35 Chemistry: #/programs/BJy5pm0M4?bc=true&bcCurrent=Chemistry&bcItemType=programs
36 Chemistry: #/programs/Bkj8a7RzE?bc=true&bcCurrent=Chemistry&bcItemType=programs
37 Chemistry: #/programs/rkj86XCf4?bc=true&bcCurrent=Chemistry&bcItemType=programs
38 Chemistry and Earth Sciences: #/programs/B1aUamCGV?bc=true&bcCurrent=Chemistry%20and%20Earth%20Sciences&bcItemType=programs
39 Chemistry and Earth Sciences: #/programs/Hy6Ia7CGN?bc=true&bcCurrent=Chemistry%20and%20Earth%20Sciences&bcItemType=programs
40 Chemistry and Mathematics: #/programs/BJn8p7AGV?bc=true&bcCurrent=Chemistry%20and%20Mathematics&bcItemType=programs
41 Chemistry and Mathematics: #/programs/SknLp7RfV?bc=true&bcCurrent=Chemistry%20and%20Mathematics&bcItemType=programs
42 Chemistry and Ocean Sciences: #/programs/HJ1xpFYIH?bc=true&bcCurrent=Chemistry%20and%20Ocean%20Sciences&bcItemType=programs
43 Chemistry and Ocean Sciences: #/programs/Skmk6dt8r?bc=true&bcCurrent=Chemistry%20and%20Ocean%20Sciences&bcItemType=programs
44 Chemistry for the Medical Sciences: #/programs/Byty_vt8S?bc=true&bcCurrent=Chemistry%20for%20the%20Medical%20Sciences&bcItemType=programs
45 Chemistry for the Medical Sciences: #/programs/S1nLT7CME?bc=true&bcCurrent=Chemistry%20for%20the%20Medical%20Sciences&bcItemType=programs
46 Child and Youth Care: #/programs/rylJr67RMV?bc=true&bcCurrent=Child%20and%20Youth%20Care&bcItemType=programs
47 Chinese Studies: #/programs/BkjtTmAzE?bc=true&bcCurrent=Chinese%20Studies&bcItemType=programs
48 Civil Engineering: #/programs/HkuEpmCzV?bc=true&bcCurrent=Civil%20Engineering&bcItemType=programs
49 Civil Law: #/programs/r1P8TXRfE?bc=true&bcCurrent=Civil%20Law&bcItemType=programs
50 Climate Science: #/programs/H1dHTmAAP?bc=true&bcCurrent=Climate%20Science&bcItemType=programs
51 Climate Science: #/programs/Hk0--QRAP?bc=true&bcCurrent=Climate%20Science&bcItemType=programs
52 Coastal Studies: #/programs/SkeNqamCGE?bc=true&bcCurrent=Coastal%20Studies&bcItemType=programs
53 Collections Management: #/programs/H1BOTQAfV?bc=true&bcCurrent=Collections%20Management&bcItemType=programs
54 Commerce: #/programs/rJgEpXAz4?bc=true&bcCurrent=Commerce&bcItemType=programs
55 Composition and Theory: #/programs/S1l9V6mCfV?bc=true&bcCurrent=Composition%20and%20Theory&bcItemType=programs
56 Computer Engineering: #/programs/ryuNpXRfE?bc=true&bcCurrent=Computer%20Engineering&bcItemType=programs
57 Computer Science: #/programs/B1gkKa70z4?bc=true&bcCurrent=Computer%20Science&bcItemType=programs
58 Computer Science: #/programs/Bkl7ET7CMN?bc=true&bcCurrent=Computer%20Science&bcItemType=programs
59 Computer Science: #/programs/H1kK6QAGE?bc=true&bcCurrent=Computer%20Science&bcItemType=programs
60 Computer Science: #/programs/r1X46XCfE?bc=true&bcCurrent=Computer%20Science&bcItemType=programs
61 Computer Science and Health Information Science: #/programs/BJHE6QAGV?bc=true&bcCurrent=Computer%20Science%20and%20Health%20Information%20Science&bcItemType=programs
62 Computer Science and Mathematics: #/programs/BkENT7RzV?bc=true&bcCurrent=Computer%20Science%20and%20Mathematics&bcItemType=programs
63 Computer Science and Mathematics: #/programs/H1lm4T7AfN?bc=true&bcCurrent=Computer%20Science%20and%20Mathematics&bcItemType=programs
64 Computer Systems: #/programs/HygYaXAfN?bc=true&bcCurrent=Computer%20Systems&bcItemType=programs
65 Creative Writing: #/programs/SJzKpXRMN?bc=true&bcCurrent=Creative%20Writing&bcItemType=programs
66 Cultural Resource Management: #/programs/r1EuamRMV?bc=true&bcCurrent=Cultural%20Resource%20Management&bcItemType=programs
67 Data Science: #/programs/SkH4Tm0zN?bc=true&bcCurrent=Data%20Science&bcItemType=programs
68 Data Science: #/programs/Syl44aQAGV?bc=true&bcCurrent=Data%20Science&bcItemType=programs
69 Data Science: #/programs/rygAaQRfN?bc=true&bcCurrent=Data%20Science&bcItemType=programs
70 Digital and Interactive Media in the Arts: #/programs/rJeftTQAMV?bc=true&bcCurrent=Digital%20and%20Interactive%20Media%20in%20the%20Arts&bcItemType=programs
71 Earth Sciences: #/programs/Hk08T7RG4?bc=true&bcCurrent=Earth%20Sciences&bcItemType=programs
72 Earth Sciences: #/programs/Hkxyq67AzE?bc=true&bcCurrent=Earth%20Sciences&bcItemType=programs
73 Earth Sciences: #/programs/SkxTLa7AfV?bc=true&bcCurrent=Earth%20Sciences&bcItemType=programs
74 Economics: #/programs/B1x2waX0z4?bc=true&bcCurrent=Economics&bcItemType=programs
75 Economics: #/programs/H13v6mAME?bc=true&bcCurrent=Economics&bcItemType=programs
76 Economics: #/programs/HJavTQCzE?bc=true&bcCurrent=Economics&bcItemType=programs
77 Economics: #/programs/SJMc6mCz4?bc=true&bcCurrent=Economics&bcItemType=programs
78 Economics: #/programs/r1hv6QRG4?bc=true&bcCurrent=Economics&bcItemType=programs
79 Education: #/programs/B10O6Q0MV?bc=true&bcCurrent=Education&bcItemType=programs
80 Electrical Engineering: #/programs/ryK4am0MV?bc=true&bcCurrent=Electrical%20Engineering&bcItemType=programs
81 Electrical Systems: #/programs/r1xlt6mAM4?bc=true&bcCurrent=Electrical%20Systems&bcItemType=programs
82 Elementary Curriculum: #/programs/H1WEpXRMN?bc=true&bcCurrent=Elementary%20Curriculum&bcItemType=programs
83 English: #/programs/BJvtpmAG4?bc=true&bcCurrent=English&bcItemType=programs
84 English: #/programs/HJfBTmCGV?bc=true&bcCurrent=English&bcItemType=programs
85 English: #/programs/HkMHTXRz4?bc=true&bcCurrent=English&bcItemType=programs
86 Environmental Studies: #/programs/HygTw67AzV?bc=true&bcCurrent=Environmental%20Studies&bcItemType=programs
87 Environmental Studies: #/programs/SkQqTQ0ME?bc=true&bcCurrent=Environmental%20Studies&bcItemType=programs
88 European Studies: #/programs/SJQFpmRGV?bc=true&bcCurrent=European%20Studies&bcItemType=programs
89 Film Studies: #/programs/HkgXYamRfV?bc=true&bcCurrent=Film%20Studies&bcItemType=programs
90 Financial Mathematics and Economics: #/programs/Hk_wpQAGE?bc=true&bcCurrent=Financial%20Mathematics%20and%20Economics&bcItemType=programs
91 Financial Mathematics and Economics: #/programs/ryQOpe2qC?bc=true&bcCurrent=Financial%20Mathematics%20and%20Economics&bcItemType=programs
92 Foundations in Indigenous Fine Arts: #/programs/SkVuamRzE?bc=true&bcCurrent=Foundations%20in%20Indigenous%20Fine%20Arts&bcItemType=programs
93 French and Francophone Studies: #/programs/H18cam0zV?bc=true&bcCurrent=French%20and%20Francophone%20Studies&bcItemType=programs
94 French and Francophone Studies: #/programs/B1mBpXRGN?bc=true&bcCurrent=French%20and%20Francophone%20Studies&bcItemType=programs
95 French and Francophone Studies: #/programs/H1mHp7RMV?bc=true&bcCurrent=French%20and%20Francophone%20Studies&bcItemType=programs
96 Gender Studies: #/programs/BJvS6mAzE?bc=true&bcCurrent=Gender%20Studies&bcItemType=programs
97 Gender Studies: #/programs/BkISaQCMV?bc=true&bcCurrent=Gender%20Studies&bcItemType=programs
98 Gender Studies: #/programs/H18Qqa55D?bc=true&bcCurrent=Gender%20Studies&bcItemType=programs
99 Gender Studies: #/programs/r1lDYaXRzV?bc=true&bcCurrent=Gender%20Studies&bcItemType=programs
100 Geographic Information Technology: #/programs/Byr9TXCfN?bc=true&bcCurrent=Geographic%20Information%20Technology&bcItemType=programs
101 Geography: #/programs/H1e0D6Q0GN?bc=true&bcCurrent=Geography&bcItemType=programs
102 Geography: #/programs/HJ0PTX0zE?bc=true&bcCurrent=Geography&bcItemType=programs
103 Geography: #/programs/HJ0PpmRfE?bc=true&bcCurrent=Geography&bcItemType=programs
104 Geography: #/programs/Hk-pwaX0G4?bc=true&bcCurrent=Geography&bcItemType=programs
105 Geography and Computer Science (Geomatics): #/programs/r1gHEpQAf4?bc=true&bcCurrent=Geography%20and%20Computer%20Science%20(Geomatics)&bcItemType=programs
106 Geography BA: #/programs/rJQc6mRMN?bc=true&bcCurrent=Geography%20BA&bcItemType=programs
107 Geography BSc: #/programs/ryV9TQ0fN?bc=true&bcCurrent=Geography%20BSc&bcItemType=programs
108 Germanic Studies: #/programs/HkNrp7CGN?bc=true&bcCurrent=Germanic%20Studies&bcItemType=programs
109 Germanic Studies: #/programs/SkPtTmCMN?bc=true&bcCurrent=Germanic%20Studies&bcItemType=programs
110 Germanic Studies: #/programs/rJBSp7CM4?bc=true&bcCurrent=Germanic%20Studies&bcItemType=programs
111 Global Development Studies: #/programs/H10O6XCfE?bc=true&bcCurrent=Global%20Development%20Studies&bcItemType=programs
112 Greek and Latin Language and Literature: #/programs/B1BBam0fV?bc=true&bcCurrent=Greek%20and%20Latin%20Language%20and%20Literature&bcItemType=programs
113 Greek and Latin Language and Literature: #/programs/rkSrpmRGN?bc=true&bcCurrent=Greek%20and%20Latin%20Language%20and%20Literature&bcItemType=programs
114 Greek and Roman Studies: #/programs/BkUSTm0M4?bc=true&bcCurrent=Greek%20and%20Roman%20Studies&bcItemType=programs
115 Greek and Roman Studies: #/programs/HkOF6XRGE?bc=true&bcCurrent=Greek%20and%20Roman%20Studies&bcItemType=programs
116 Greek and Roman Studies: #/programs/SyUrpX0MV?bc=true&bcCurrent=Greek%20and%20Roman%20Studies&bcItemType=programs
117 Health and Society: #/programs/HJpdaQAz4?bc=true&bcCurrent=Health%20and%20Society&bcItemType=programs
118 Health Information Science: #/programs/SkxH6X0z4?bc=true&bcCurrent=Health%20Information%20Science&bcItemType=programs
119 Hispanic Studies: #/programs/B1xuK6Q0MV?bc=true&bcCurrent=Hispanic%20Studies&bcItemType=programs
120 Hispanic Studies: #/programs/HysHamCME?bc=true&bcCurrent=Hispanic%20Studies&bcItemType=programs
121 Hispanic Studies: #/programs/SJnBp7Az4?bc=true&bcCurrent=Hispanic%20Studies&bcItemType=programs
122 History: #/programs/HyaSp7AGN?bc=true&bcCurrent=History&bcItemType=programs
123 History: #/programs/SyFYTXCfV?bc=true&bcCurrent=History&bcItemType=programs
124 History: #/programs/r1CHaQCMN?bc=true&bcCurrent=History&bcItemType=programs
125 Indigenous Community Development and Governance: #/programs/SJLd6QAMN?bc=true&bcCurrent=Indigenous%20Community%20Development%20and%20Governance&bcItemType=programs
126 Indigenous Community Development and Governance: #/programs/rJAgC5-kK?bc=true&bcCurrent=Indigenous%20Community%20Development%20and%20Governance&bcItemType=programs
127 Indigenous Community Development and Governance: #/programs/S1DQhiWkt?bc=true&bcCurrent=Indigenous%20Community%20Development%20and%20Governance%20&bcItemType=programs
128 Indigenous Language Proficiency: #/programs/ryeeAp7AzV?bc=true&bcCurrent=Indigenous%20Language%20Proficiency&bcItemType=programs
129 Indigenous Language Proficiency in SENĆOŦEN: #/programs/BJs-48ZIi?bc=true&bcCurrent=Indigenous%20Language%20Proficiency%20in%20SEN%C4%86O%C5%A6EN&bcItemType=programs
130 Indigenous Language Revitalization: #/programs/HJg4a7RGN?bc=true&bcCurrent=Indigenous%20Language%20Revitalization&bcItemType=programs
131 Indigenous Language Revitalization: #/programs/SyEdTmAME?bc=true&bcCurrent=Indigenous%20Language%20Revitalization&bcItemType=programs
132 Indigenous Language Revitalization: #/programs/SytOTQ0zN?bc=true&bcCurrent=Indigenous%20Language%20Revitalization&bcItemType=programs
133 Indigenous Studies: #/programs/HyRBaXAfE?bc=true&bcCurrent=Indigenous%20Studies&bcItemType=programs
134 Indigenous Studies: #/programs/S1qYpQ0zV?bc=true&bcCurrent=Indigenous%20Studies&bcItemType=programs
135 Information Communication Technology: #/programs/HkMd6m0zN?bc=true&bcCurrent=Information%20Communication%20Technology&bcItemType=programs
136 Intercultural Studies and Practice: #/programs/r1xQOamAMN?bc=true&bcCurrent=Intercultural%20Studies%20and%20Practice&bcItemType=programs
137 Japanese Studies: #/programs/SJxitpmAzN?bc=true&bcCurrent=Japanese%20Studies&bcItemType=programs
138 Kinesiology: #/programs/S1MNp7CMV?bc=true&bcCurrent=Kinesiology&bcItemType=programs
139 Kinesiology: #/programs/rkfEamRG4?bc=true&bcCurrent=Kinesiology&bcItemType=programs
140 Language and Cultural Proficiency: Chinese: #/programs/ByYd6XCME?bc=true&bcCurrent=Language%20and%20Cultural%20Proficiency%3A%20Chinese&bcItemType=programs
141 Language and Cultural Proficiency: French: #/programs/S1lKO6m0zN?bc=true&bcCurrent=Language%20and%20Cultural%20Proficiency%3A%20French&bcItemType=programs
142 Language and Cultural Proficiency: German: #/programs/Hy5_67RGV?bc=true&bcCurrent=Language%20and%20Cultural%20Proficiency%3A%20German&bcItemType=programs
143 Language and Cultural Proficiency: Japanese: #/programs/BJYuT7Cf4?bc=true&bcCurrent=Language%20and%20Cultural%20Proficiency%3A%20Japanese&bcItemType=programs
144 Language and Cultural Proficiency: Russian: #/programs/B1eqd6Q0fE?bc=true&bcCurrent=Language%20and%20Cultural%20Proficiency%3A%20Russian&bcItemType=programs
145 Language and Cultural Proficiency: Spanish: #/programs/B1jO6QRz4?bc=true&bcCurrent=Language%20and%20Cultural%20Proficiency%3A%20Spanish&bcItemType=programs
146 Latin American Studies: #/programs/B11Ipm0G4?bc=true&bcCurrent=Latin%20American%20Studies&bcItemType=programs
147 Latin American Studies: #/programs/B1yLTXRGE?bc=true&bcCurrent=Latin%20American%20Studies&bcItemType=programs
148 Latin American Studies: #/programs/S1eqt6QCzV?bc=true&bcCurrent=Latin%20American%20Studies&bcItemType=programs
149 Law: #/programs/H1BLpmAGN?bc=true&bcCurrent=Law&bcItemType=programs
150 Law: #/programs/H1IIam0fN?bc=true&bcCurrent=Law&bcItemType=programs
151 Law and Business Administration: #/programs/HkUI670fE?bc=true&bcCurrent=Law%20and%20Business%20Administration&bcItemType=programs
152 Law and Public Administration: #/programs/B1DU6mAzV?bc=true&bcCurrent=Law%20and%20Public%20Administration&bcItemType=programs
153 Linguistics: #/programs/BylITXCGE?bc=true&bcCurrent=Linguistics&bcItemType=programs
154 Linguistics: #/programs/HkIz9sen4?bc=true&bcCurrent=Linguistics&bcItemType=programs
155 Linguistics: #/programs/SklUTm0fE?bc=true&bcCurrent=Linguistics&bcItemType=programs
156 Linguistics: #/programs/SyqtpmCzE?bc=true&bcCurrent=Linguistics&bcItemType=programs
157 Linguistics: #/programs/rJ_P5jgnE?bc=true&bcCurrent=Linguistics&bcItemType=programs
158 Local Government Management: #/programs/ByeIdpXCM4?bc=true&bcCurrent=Local%20Government%20Management&bcItemType=programs
159 Local Government Management: #/programs/H1vOTmAME?bc=true&bcCurrent=Local%20Government%20Management&bcItemType=programs
160 Mathematics: #/programs/Bkl56XCz4?bc=true&bcCurrent=Mathematics&bcItemType=programs
161 Mathematics: #/programs/HJegqp70MN?bc=true&bcCurrent=Mathematics&bcItemType=programs
162 Mathematics: #/programs/SkHDTQRzE?bc=true&bcCurrent=Mathematics&bcItemType=programs
163 Mathematics: #/programs/r1XvamCzN?bc=true&bcCurrent=Mathematics&bcItemType=programs
164 Mathematics: #/programs/rkND67RfV?bc=true&bcCurrent=Mathematics&bcItemType=programs
165 Mathematics: #/programs/ryEwp70GN?bc=true&bcCurrent=Mathematics&bcItemType=programs
166 Mathematics and Statistics: #/programs/BkDwpQAf4?bc=true&bcCurrent=Mathematics%20and%20Statistics&bcItemType=programs
167 Mathematics and Statistics: #/programs/HJlvvaXAfV?bc=true&bcCurrent=Mathematics%20and%20Statistics&bcItemType=programs
168 Mechanical Engineering: #/programs/SkYVTmCzE?bc=true&bcCurrent=Mechanical%20Engineering&bcItemType=programs
169 Mechanical Systems: #/programs/rygFTQRzE?bc=true&bcCurrent=Mechanical%20Systems&bcItemType=programs
170 Media Studies: #/programs/rJP4a8byi?bc=true&bcCurrent=Media%20Studies&bcItemType=programs
171 Medieval Studies: #/programs/BJWL6mRM4?bc=true&bcCurrent=Medieval%20Studies&bcItemType=programs
172 Medieval Studies: #/programs/SyG8TmRzN?bc=true&bcCurrent=Medieval%20Studies&bcItemType=programs
173 Medieval Studies: #/programs/r1jFa7CME?bc=true&bcCurrent=Medieval%20Studies&bcItemType=programs
174 Microbiology: #/programs/Bk0F6QAGV?bc=true&bcCurrent=Microbiology&bcItemType=programs
175 Microbiology: #/programs/ByRI6X0z4?bc=true&bcCurrent=Microbiology&bcItemType=programs
176 Microbiology: #/programs/r1x0LT7CzE?bc=true&bcCurrent=Microbiology&bcItemType=programs
177 Microbiology and Chemistry: #/programs/BykPpQCGV?bc=true&bcCurrent=Microbiology%20and%20Chemistry&bcItemType=programs
178 Microbiology and Chemistry: #/programs/SJ-mSBp-Y?bc=true&bcCurrent=Microbiology%20and%20Chemistry&bcItemType=programs
179 Museum Studies: #/programs/HJEFaXAGN?bc=true&bcCurrent=Museum%20Studies&bcItemType=programs
180 Music: #/programs/BJNKaQCz4?bc=true&bcCurrent=Music&bcItemType=programs
181 Music: #/programs/BkXNrzIDv?bc=true&bcCurrent=Music&bcItemType=programs
182 Music and Computer Science: #/programs/rJ8Nam0GN?bc=true&bcCurrent=Music%20and%20Computer%20Science&bcItemType=programs
183 Music and Computer Science: #/programs/ryO7UEx9V?bc=true&bcCurrent=Music%20and%20Computer%20Science&bcItemType=programs
184 Music Education: #/programs/B1nETQAf4?bc=true&bcCurrent=Music%20Education&bcItemType=programs
185 Musical Arts: #/programs/SyjN67AfN?bc=true&bcCurrent=Musical%20Arts&bcItemType=programs
186 Musicology and Sound Studies: #/programs/SJiV670zE?bc=true&bcCurrent=Musicology%20and%20Sound%20Studies&bcItemType=programs
187 Nursing: #/programs/ByxxramAM4?bc=true&bcCurrent=Nursing&bcItemType=programs
188 Ocean Sciences: #/programs/Hk1caX0zV?bc=true&bcCurrent=Ocean%20Sciences&bcItemType=programs
189 Pacific and Asian Studies: #/programs/HyhYamAf4?bc=true&bcCurrent=Pacific%20and%20Asian%20Studies&bcItemType=programs
190 Pacific and Asian Studies: #/programs/Sy7IaX0M4?bc=true&bcCurrent=Pacific%20and%20Asian%20Studies&bcItemType=programs
191 Pacific and Asian Studies: #/programs/r1Q8amAz4?bc=true&bcCurrent=Pacific%20and%20Asian%20Studies&bcItemType=programs
192 Performance: #/programs/S1jEp7AM4?bc=true&bcCurrent=Performance&bcItemType=programs
193 Philosophy: #/programs/BJEUa7RGE?bc=true&bcCurrent=Philosophy&bcItemType=programs
194 Philosophy: #/programs/Bk4UpQRfV?bc=true&bcCurrent=Philosophy&bcItemType=programs
195 Philosophy: #/programs/Syl3tTXAfE?bc=true&bcCurrent=Philosophy&bcItemType=programs
196 Physical and Health Education: #/programs/HkwgwBMHB?bc=true&bcCurrent=Physical%20and%20Health%20Education&bcItemType=programs
197 Physical Education: #/programs/HJ7iMZfa4?bc=true&bcCurrent=Physical%20Education&bcItemType=programs
198 Physical Geography and Earth and Ocean Sciences: #/programs/H1QwamAzE?bc=true&bcCurrent=Physical%20Geography%20and%20Earth%20and%20Ocean%20Sciences&bcItemType=programs
199 Physical Geography and Earth and Ocean Sciences: #/programs/SkMPTX0M4?bc=true&bcCurrent=Physical%20Geography%20and%20Earth%20and%20Ocean%20Sciences&bcItemType=programs
200 Physics: #/programs/B1b9670GE?bc=true&bcCurrent=Physics&bcItemType=programs
201 Physics: #/programs/BJYw6mCzE?bc=true&bcCurrent=Physics&bcItemType=programs
202 Physics: #/programs/HyW9pmRGN?bc=true&bcCurrent=Physics&bcItemType=programs
203 Physics: #/programs/rkOD6m0GE?bc=true&bcCurrent=Physics&bcItemType=programs
204 Physics and Astronomy: #/programs/B19DpXAfE?bc=true&bcCurrent=Physics%20and%20Astronomy&bcItemType=programs
205 Physics and Astronomy: #/programs/SkcDaQRzV?bc=true&bcCurrent=Physics%20and%20Astronomy&bcItemType=programs
206 Physics and Biochemistry: #/programs/B1Y8TXAG4?bc=true&bcCurrent=Physics%20and%20Biochemistry&bcItemType=programs
207 Physics and Biochemistry: #/programs/ryOU6Q0zV?bc=true&bcCurrent=Physics%20and%20Biochemistry&bcItemType=programs
208 Physics and Computer Science: #/programs/HJU4TQCM4?bc=true&bcCurrent=Physics%20and%20Computer%20Science&bcItemType=programs
209 Physics and Computer Science: #/programs/SJxIV67Cz4?bc=true&bcCurrent=Physics%20and%20Computer%20Science&bcItemType=programs
210 Physics and Earth Sciences (Geophysics): #/programs/B1kw6QAfV?bc=true&bcCurrent=Physics%20and%20Earth%20Sciences%20(Geophysics)&bcItemType=programs
211 Physics and Earth Sciences (Geophysics): #/programs/rylJwpXCME?bc=true&bcCurrent=Physics%20and%20Earth%20Sciences%20(Geophysics)&bcItemType=programs
212 Physics and Mathematics: #/programs/H1Ovpm0ME?bc=true&bcCurrent=Physics%20and%20Mathematics&bcItemType=programs
213 Physics and Ocean-Atmosphere Sciences: #/programs/BygDaXAfV?bc=true&bcCurrent=Physics%20and%20Ocean-Atmosphere%20Sciences&bcItemType=programs
214 Physics and Ocean-Atmosphere Sciences: #/programs/S1evaXCzE?bc=true&bcCurrent=Physics%20and%20Ocean-Atmosphere%20Sciences&bcItemType=programs
215 Political Science: #/programs/HkJ_aX0f4?bc=true&bcCurrent=Political%20Science&bcItemType=programs
216 Political Science: #/programs/HyH9pmRzN?bc=true&bcCurrent=Political%20Science&bcItemType=programs
217 Political Science: #/programs/rkJup70zE?bc=true&bcCurrent=Political%20Science&bcItemType=programs
218 Post-Degree Professional Program (Elementary): #/programs/BJZ4amRzN?bc=true&bcCurrent=Post-Degree%20Professional%20Program%20(Elementary)&bcItemType=programs
219 Post-Degree Professional Program (Indigenous Education - Elementary): #/programs/B1cw8DmUv?bc=true&bcCurrent=Post-Degree%20Professional%20Program%20(Indigenous%20Education%20-%20Elementary)&bcItemType=programs
220 Post-Degree Professional Program (Middle Years): #/programs/rJWEpmCfV?bc=true&bcCurrent=Post-Degree%20Professional%20Program%20(Middle%20Years)&bcItemType=programs
221 Post-Degree Professional Program (Secondary): #/programs/HJZ61cHrB?bc=true&bcCurrent=Post-Degree%20Professional%20Program%20(Secondary)&bcItemType=programs
222 Professional Communication: #/programs/S1LtaXRzN?bc=true&bcCurrent=Professional%20Communication&bcItemType=programs
223 Professional Writing in Journalism and Publishing: #/programs/BJ4FTXCME?bc=true&bcCurrent=Professional%20Writing%20in%20Journalism%20and%20Publishing&bcItemType=programs
224 Psychology: #/programs/B1euTXAfN?bc=true&bcCurrent=Psychology&bcItemType=programs
225 Psychology: #/programs/H1-_6QCzV?bc=true&bcCurrent=Psychology&bcItemType=programs
226 Psychology: #/programs/HJgyOpQRz4?bc=true&bcCurrent=Psychology&bcItemType=programs
227 Psychology: #/programs/HkB5p7AfN?bc=true&bcCurrent=Psychology&bcItemType=programs
228 Psychology: #/programs/HyxeOTQCfV?bc=true&bcCurrent=Psychology&bcItemType=programs
229 Psychology and Computer Science: #/programs/ByPE6QRzE?bc=true&bcCurrent=Psychology%20and%20Computer%20Science&bcItemType=programs
230 Public Administration: #/programs/ry8YaXRzE?bc=true&bcCurrent=Public%20Administration&bcItemType=programs
231 Public Health: #/programs/SygSTmRzN?bc=true&bcCurrent=Public%20Health&bcItemType=programs
232 Public Policy and Governance: #/programs/rJDdTQAzV?bc=true&bcCurrent=Public%20Policy%20and%20Governance&bcItemType=programs
233 Public Sector Management: #/programs/S1LOp70G4?bc=true&bcCurrent=Public%20Sector%20Management&bcItemType=programs
234 Public Sector Management: #/programs/ry_da7RGN?bc=true&bcCurrent=Public%20Sector%20Management&bcItemType=programs
235 Recreation and Health Education: #/programs/S17NaXCfV?bc=true&bcCurrent=Recreation%20and%20Health%20Education&bcItemType=programs
236 Recreation and Health Education: #/programs/SyefV6QRGV?bc=true&bcCurrent=Recreation%20and%20Health%20Education&bcItemType=programs
237 Religion, Culture and Society: #/programs/H1xEUTm0f4?bc=true&bcCurrent=Religion%2C%20Culture%20and%20Society&bcItemType=programs
238 Religion, Culture and Society: #/programs/rJpF6QRG4?bc=true&bcCurrent=Religion%2C%20Culture%20and%20Society&bcItemType=programs
239 Restoration of Natural Systems: #/programs/B1hu6Q0MN?bc=true&bcCurrent=Restoration%20of%20Natural%20Systems&bcItemType=programs
240 Slavic Studies: #/programs/Hk_Kp7CzV?bc=true&bcCurrent=Slavic%20Studies&bcItemType=programs
241 Slavic Studies: #/programs/SyS8aX0G4?bc=true&bcCurrent=Slavic%20Studies&bcItemType=programs
242 Slavic Studies: #/programs/SylE8aXRfN?bc=true&bcCurrent=Slavic%20Studies&bcItemType=programs
243 Social Justice Studies: #/programs/B1Td67AMN?bc=true&bcCurrent=Social%20Justice%20Studies&bcItemType=programs
244 Social Justice Studies: #/programs/B1wqpQCz4?bc=true&bcCurrent=Social%20Justice%20Studies&bcItemType=programs
245 Social Work: #/programs/BJZBaQAzN?bc=true&bcCurrent=Social%20Work&bcItemType=programs
246 Sociology: #/programs/B1I96mCfN?bc=true&bcCurrent=Sociology&bcItemType=programs
247 Sociology: #/programs/BygW_TXAMN?bc=true&bcCurrent=Sociology&bcItemType=programs
248 Sociology: #/programs/Hybd67RzV?bc=true&bcCurrent=Sociology&bcItemType=programs
249 Software Development: #/programs/HJZYaXCG4?bc=true&bcCurrent=Software%20Development&bcItemType=programs
250 Software Engineering: #/programs/SJKVp7AME?bc=true&bcCurrent=Software%20Engineering&bcItemType=programs
251 Southeast Asian Studies: #/programs/Sk2F6mRfE?bc=true&bcCurrent=Southeast%20Asian%20Studies&bcItemType=programs
252 Special and Inclusive Education: #/programs/H1mOT70GE?bc=true&bcCurrent=Special%20and%20Inclusive%20Education&bcItemType=programs
253 Special and Inclusive Education: #/programs/SJX_TX0GV?bc=true&bcCurrent=Special%20and%20Inclusive%20Education&bcItemType=programs
254 Statistics: #/programs/BJl9TXRfV?bc=true&bcCurrent=Statistics&bcItemType=programs
255 Statistics: #/programs/BkIP6mCME?bc=true&bcCurrent=Statistics&bcItemType=programs
256 Statistics: #/programs/BkUPp7RfV?bc=true&bcCurrent=Statistics&bcItemType=programs
257 Statistics: #/programs/H1lqaXRz4?bc=true&bcCurrent=Statistics&bcItemType=programs
258 Statistics: #/programs/SkerDT7Rz4?bc=true&bcCurrent=Statistics&bcItemType=programs
259 Technology and Society: #/programs/ByrFam0MN?bc=true&bcCurrent=Technology%20and%20Society&bcItemType=programs
260 Theatre: #/programs/H1x3N6QAMN?bc=true&bcCurrent=Theatre&bcItemType=programs
261 Theatre: #/programs/ryeSKp7CMV?bc=true&bcCurrent=Theatre&bcItemType=programs
262 Theatre History: #/programs/Hy3V67AfV?bc=true&bcCurrent=Theatre%20History&bcItemType=programs
263 Transformative Climate Action: #/programs/BJj8RZyNj?bc=true&bcCurrent=Transformative%20Climate%20Action&bcItemType=programs
264 Visitor and Community Engagement: #/programs/H1e0am0M4?bc=true&bcCurrent=Visitor%20and%20Community%20Engagement&bcItemType=programs
265 Visual Arts: #/programs/HJRNamRfN?bc=true&bcCurrent=Visual%20Arts&bcItemType=programs
266 Visual Arts: #/programs/HJpN6Q0zE?bc=true&bcCurrent=Visual%20Arts&bcItemType=programs
267 Visual Arts: #/programs/HkHKpm0fV?bc=true&bcCurrent=Visual%20Arts&bcItemType=programs
268 Visual Arts and Computer Science: #/programs/B1ap-HzqN?bc=true&bcCurrent=Visual%20Arts%20and%20Computer%20Science&bcItemType=programs
269 Visual Arts and Computer Science: #/programs/ByDE6XAM4?bc=true&bcCurrent=Visual%20Arts%20and%20Computer%20Science&bcItemType=programs
270 Voluntary and Non-profit Sector Management: #/programs/r1_OT7RGE?bc=true&bcCurrent=Voluntary%20and%20Non-profit%20Sector%20Management&bcItemType=programs
271 West Shore Computing Gateway: #/programs/BJfAswALT?bc=true&bcCurrent=West%20Shore%20Computing%20Gateway&bcItemType=programs
272 Writing: #/programs/H11BaQ0M4?bc=true&bcCurrent=Writing&bcItemType=programs
273 Writing: #/programs/H1JB6mAzV?bc=true&bcCurrent=Writing&bcItemType=programs
"""

majors_pids = []

for line in data.strip().splitlines():
    parts = line.strip().split(':', 1)
    if len(parts) == 2:
        name = parts[0].split(maxsplit=1)[1].strip()
        link = parts[1].strip()
        # Filter: skip things like 'Minor', 'Certificate' if needed
        # (Or keep all if you're unsure)
        match = re.search(r'/programs/([^?]+)', link)
        if match:
            pid = match.group(1)
            majors_pids.append({'name': name, 'pid': pid})

# Print out
for item in majors_pids:
    print(f"{item['name']}: {item['pid']}")
