import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('lecture.html', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Section titles inside mcq-section h3
    ('اسئلة MCQ — المجهر وعلم الأنسجة', 'MCQ Questions — Microscopy &amp; Histology'),
    ('اسئلة MCQ — مستويات جسم الإنسان', 'MCQ Questions — Levels of Human Body Organization'),
    ('اسئلة MCQ — الخلية ومكوناتها', 'MCQ Questions — The Cell &amp; Its Components'),
    ('اسئلة MCQ — تصنيف العضيات', 'MCQ Questions — Classification of Organelles'),
    ('اسئلة MCQ — غشاء الخلية', 'MCQ Questions — Cell Membrane'),
    ('اسئلة MCQ — الميتوكوندريا', 'MCQ Questions — Mitochondria'),
    ('اسئلة MCQ — الشبكة الإندوبلازمية', 'MCQ Questions — Endoplasmic Reticulum'),
    ('اسئلة MCQ — جهاز جولجي', 'MCQ Questions — Golgi Apparatus'),

    # Q1
    ('1. ما مصدر الاضاءة في المجهر الإلكتروني؟', '1. What is the source of illumination in the Electron Microscope?'),
    ('اشعة ضوئية', 'Light rays'),
    ('حزمة الكترونات', 'Electron beam'),
    ('اشعة تحت الحمراء', 'Infrared rays'),
    ('الاشعة فوق البنفسجية', 'Ultraviolet rays'),
    ('الصواب: المجهر الإلكتروني يستخدم <b>حزمة الكترونات (Electron beam)</b>، بينما المجهر الضوئي يستخدم الاشعة الضوئية.',
     'Correct: The Electron Microscope uses an <b>Electron beam</b>, while the Light Microscope uses light rays.'),

    # Q2
    ('2. ما هي اقصى قوة تكبير للمجهر الضوئي؟', '2. What is the maximum magnifying power of the Light Microscope?'),
    ('المجهر الضوئي يكبر حتى <b>×1500–2000</b>، بينما المجهر الإلكتروني ×10,000 واكبر بكثير.',
     'The Light Microscope magnifies up to <b>×1500–2000</b>, while the Electron Microscope reaches ×10,000 and much more.'),

    # Q3
    ('3. ما الذي يُستخدم المجهر الإلكتروني لفحصه؟', '3. What is the Electron Microscope used to examine?'),
    ('الانسجة كاملة', 'Whole tissues'),
    ('الخلايا كاملة', 'Whole cells'),
    ('العضيات داخل الخلية (Intracellular organelles)', 'Intracellular organelles'),
    ('الاعضاء بالعين المجردة', 'Organs with the naked eye'),
    ('المجهر الإلكتروني يُستخدم لفحص <b>العضيات الداخلية للخلية (Intracellular organelles)</b> لانه يكبر اكثر بكثير.',
     'The Electron Microscope is used to examine <b>Intracellular organelles</b> because it magnifies much more.'),

    # Q4
    ('4. ما الصبغة الاساسية المستخدمة مع المجهر الضوئي؟', '4. What is the main stain used with the Light Microscope?'),
    ('الصبغة الاساسية للمجهر الضوئي هي <b>H&amp;E (Hematoxylin + Eosin)</b>.',
     'The main stain for the Light Microscope is <b>H&amp;E (Hematoxylin + Eosin)</b>.'),

    # Q5
    ('5. ما الترتيب الصحيح من الاصغر الى الاكبر في تنظيم جسم الإنسان؟',
     '5. What is the correct order from smallest to largest in human body organization?'),
    ('الترتيب الصحيح: <b>Cells → Tissues → Organs → Systems → Human Body</b>. الخلية هي اصغر وحدة وجسم الإنسان هو الاكبر.',
     'Correct order: <b>Cells → Tissues → Organs → Systems → Human Body</b>. The cell is the smallest unit and the human body is the largest.'),

    # Q6
    ('6. ما مكونات المصفوفة السيتوبلازمية؟', '6. What are the constituents of the Cytoplasmic Matrix?'),
    ('DNA, RNA, Enzymes فقط', 'DNA, RNA, Enzymes only'),
    ('Glycogen, Fat, Pigments', 'Glycogen, Fat &amp; Pigments'),
    ('Mitochondria, Ribosomes, Golgi', 'Mitochondria, Ribosomes, Golgi'),
    ('المصفوفة السيتوبلازمية محلول غروي يحتوي على: <b>Proteins, Carbohydrates, Lipids, Minerals, Enzymes</b>.',
     'The Cytoplasmic Matrix is a colloid solution containing: <b>Proteins, Carbohydrates, Lipids, Minerals, Enzymes</b>.'),

    # Q7
    ('7. اي من الآتي يعد من الاحتواءات السيتوبلازمية؟',
     '7. Which of the following is a Cytoplasmic Inclusion?'),
    ('الميتوكوندريا', 'Mitochondria'),
    ('الليسوسومات', 'Lysosomes'),
    ('الجليكوجين (Glycogen)', 'Glycogen'),
    ('جهاز جولجي', 'Golgi apparatus'),
    ('<b>Glycogen</b> من الاحتواءات السيتوبلازمية (غير حي، مؤقت). الميتوكوندريا وجولجي والليسوسومات كلها عضيات.',
     '<b>Glycogen</b> is a cytoplasmic inclusion (non-living, temporary). Mitochondria, Golgi, and Lysosomes are all organelles.'),

    # Q8
    ('8. ما الخاصية التي تميز العضيات عن الاحتواءات السيتوبلازمية؟',
     '8. What is the key feature that distinguishes Organelles from Cytoplasmic Inclusions?'),
    ('العضيات مؤقتة والاحتواءات دائمة', 'Organelles are temporary and inclusions are permanent'),
    ('العضيات حية وضرورية للعمليات الحيوية', 'Organelles are living and essential for vital processes'),
    ('العضيات لا تمتلك غشاء', 'Organelles have no membrane'),
    ('العضيات مواد مخزنة', 'Organelles are stored substances'),
    ('العضيات: <b>حية، دائمة، ضرورية للعمليات الحيوية</b> كالتنفس والإفراز والهضم. الاحتواءات: غير حية، مؤقتة، غير ضرورية.',
     'Organelles are: <b>living, permanent, essential for vital processes</b> (respiration, secretion, digestion). Inclusions are: non-living, temporary, non-essential.'),

    # Q9
    ('9. اي من الآتي من العضيات الغير غشائية؟', '9. Which of the following is a Non-membranous Organelle?'),
    ('<b>الريبوسومات والهيكل الخلوي (Cytoskeleton)</b> هما العضيتان غير الغشائيتين. الباقي كله غشائي.',
     '<b>Ribosomes and the Cytoskeleton</b> are the non-membranous organelles. All others are membranous.'),

    # Q10
    ('10. Centrioles و Cilia هما من انواع اي هيكل؟',
     '10. Centrioles and Cilia are types of which structure?'),
    ('الريبوسومات', 'Ribosomes'),
    ('<b>Centrioles و Cilia</b> هما من انواع <b>Microtubules</b> التي تندرج تحت الهيكل الخلوي (Cytoskeleton).',
     '<b>Centrioles and Cilia</b> are types of <b>Microtubules</b>, which are part of the Cytoskeleton.'),

    # Q11
    ('11. ما سمك غشاء الخلية؟', '11. What is the thickness of the Cell Membrane?'),
    ('غشاء الخلية سمكه <b>8–10 nm</b> — لذلك لا يُرى بالمجهر الضوئي.',
     'The Cell Membrane is <b>8–10 nm</b> thick — that is why it is invisible under the Light Microscope.'),

    # Q12
    ('12. ما النسبة المئوية للبروتين في غشاء الخلية؟',
     '12. What is the percentage of Protein in the Cell Membrane?'),
    ('البروتين = <b>60%</b>، الدهون = 30%، الكربوهيدرات = 10%.',
     'Protein = <b>60%</b>, Lipid = 30%, Carbohydrate = 10%.'),

    # Q13
    ('13. ماذا يتكون من اتحاد Glycolipid + Glycoprotein؟',
     '13. What is formed by the combination of Glycolipid + Glycoprotein?'),
    ('Glycolipid + Glycoprotein = <b>Cell coat او Glycocalyx</b>. وهو المسؤول عن الحماية الميكانيكية والمناعة.',
     'Glycolipid + Glycoprotein = <b>Cell coat / Glycocalyx</b>. It is responsible for mechanical protection and cell immunity.'),

    # Q14
    ('14. كيف يظهر غشاء الخلية بالمجهر الإلكتروني؟',
     '14. How does the Cell Membrane appear under the Electron Microscope?'),
    ('خط واحد داكن', 'A single dark line'),
    ('ثلاثة خطوط داكنة', 'Three dark lines'),
    ('غشاء ثلاثي الطبقات (Trilamellar) — خطان داكنان يفصلهما خط فاتح', 'Trilamellar membrane — two dark parallel lines separated by a light line'),
    ('لا يظهر', 'It does not appear'),
    ('بالـ E.M يظهر كـ <b>Trilamellar membrane</b>: خطان داكنان (outer &amp; inner dark lines) يفصل بينهما خط فاتح.',
     'Under E.M it appears as a <b>Trilamellar membrane</b>: two dark lines (outer &amp; inner) separated by a light line.'),

    # Q15
    ('15. ما وظيفة الميتوكوندريا؟', '15. What is the function of Mitochondria?'),
    ('تصنيع البروتين', 'Protein synthesis'),
    ('تكوين ATP — المصدر الرئيسي للطاقة', 'Formation of ATP — the main source of energy'),
    ('إزالة السموم', 'Detoxification'),
    ('تصنيع الهرمونات', 'Hormone synthesis'),
    ('الميتوكوندريا = <b>Powerhouses of living cells</b> تصنع ATP وهو المصدر الرئيسي للطاقة.',
     'Mitochondria = <b>Powerhouses of living cells</b>. They produce ATP, which is the main source of energy.'),

    # Q16
    ('16. الطيات التي يكوّنها الغشاء الداخلي للميتوكوندريا تسمى؟',
     '16. What are the folds formed by the inner membrane of Mitochondria called?'),
    ('الغشاء الداخلي للميتوكوندريا يكوّن طيات تسمى <b>Cristae</b> وهي التي تزيد من المساحة السطحية لإنتاج الطاقة.',
     'The inner membrane of Mitochondria forms folds called <b>Cristae</b>, which increase the surface area for energy production.'),

    # Q17
    ('17. كم عدد الأغشية التي تحيط بالميتوكوندريا؟',
     '17. How many membranes surround Mitochondria?'),
    ('غشاء واحد', 'A single membrane'),
    ('غشاءان (Double membranes)', 'Two membranes (Double membranes)'),
    ('ثلاثة اغشية', 'Three membranes'),
    ('لا تملك غشاء', 'No membrane'),
    ('الميتوكوندريا محاطة بـ <b>غشاءين (Double membranes)</b>: خارجي املس وداخلي يكوّن Cristae.',
     'Mitochondria are surrounded by <b>Double membranes</b>: a smooth outer membrane and an inner membrane forming Cristae.'),

    # Q18
    ('18. ماذا تحتوي مصفوفة الميتوكوندريا (Matrix)؟',
     '18. What does the Mitochondrial Matrix contain?'),
    ('Glycogen فقط', 'Glycogen only'),
    ('بروتين ودهون فقط', 'Protein and lipids only'),
    ('ماء فقط', 'Water only'),
    ('الـ Matrix تحتوي على: <b>Lipid, Protein, Carbohydrate, Ca, Mg, DNA, RNA, Oxidative enzymes</b> — ولاحظ ان الميتوكوندريا لديها DNA خاص بها!',
     'The Matrix contains: <b>Lipid, Protein, Carbohydrate, Ca, Mg, DNA, RNA, Oxidative enzymes</b> — note that Mitochondria have their own DNA!'),

    # Q19
    ('19. ما الفرق الأساسي بين Rough ER و Smooth ER؟',
     '19. What is the main difference between Rough ER and Smooth ER?'),
    ('rER اكبر حجما', 'rER is larger in size'),
    ('rER يحمل Ribosomes على سطحه، sER لا يحمل', 'rER has Ribosomes on its surface, sER does not'),
    ('sER يحمل Ribosomes وrER لا', 'sER has Ribosomes, rER does not'),
    ('كلاهما يحمل Ribosomes', 'Both carry Ribosomes'),
    ('<b>rER (Rough ER)</b> لديه Ribosomes على سطحه الخارجي (لذلك يبدو خشنا). <b>sER (Smooth ER)</b> لا يحمل Ribosomes.',
     '<b>rER (Rough ER)</b> has Ribosomes on its outer surface (hence it appears rough). <b>sER (Smooth ER)</b> has no Ribosomes.'),

    # Q20
    ('20. في اي خلية يتواجد الـ rER بكثرة؟',
     '20. In which cells is rER (Rough ER) most abundant?'),
    ('خلايا الكبد (Liver)', 'Liver cells'),
    ('خلايا الغدد الصماء', 'Endocrine gland cells'),
    ('خلايا العضلات', 'Muscle cells'),
    ('<b>rER</b> يتواجد في الخلايا المكوِّنة للبروتين: <b>Plasma cells, Osteoblasts, Pancreas</b>.',
     '<b>rER</b> is found in protein-forming cells: <b>Plasma cells, Osteoblasts, and Pancreas</b>.'),

    # Q21
    ('21. ما وظيفة Smooth ER في الكبد؟',
     '21. What is the function of Smooth ER in the Liver?'),
    ('تصنيع البروتين', 'Protein synthesis'),
    ('تصنيع ATP', 'ATP synthesis'),
    ('ازالة سمية الكحول والادوية (Detoxification) وتخزين Glycogen',
     'Detoxification of alcohol &amp; drugs, and storage of Glycogen'),
    ('تكوين Lysosomes', 'Formation of Lysosomes'),
    ('في الكبد: <b>sER يقوم بـ Detoxification</b> (ازالة سمية الكحول والادوية) ويخزن Glycogen.',
     'In the liver: <b>sER performs Detoxification</b> (removes toxicity of alcohol &amp; drugs) and stores Glycogen.'),

    # Q22
    ('22. لماذا لا يظهر جهاز جولجي بصبغة H&amp;E؟',
     '22. Why is the Golgi Apparatus not stained by H&amp;E?'),
    ('لانه صغير جدا', 'Because it is too small'),
    ('لانه يحتوي على بروتين عالي', 'Because it has a high protein content'),
    ('لان محتواه الدهني العالي يجعله يذوب اثناء تحضير العينة', 'Because its high lipid content causes it to dissolve during specimen preparation'),
    ('لان غشاءه سميك جدا', 'Because its membrane is too thick'),
    ('جهاز جولجي يذوب اثناء تحضير العينة بسبب <b>المحتوى الدهني العالي</b> في اغشيته، لذلك يظهر كمنطقة شاحبة = <b>Negative Golgi image</b>.',
     'Golgi Apparatus dissolves during specimen preparation due to its <b>high lipid content</b>, leaving a pale area called <b>Negative Golgi image</b>.'),

    # Q23
    ('23. ما الوجه الذي يستقبل حويصلات النقل من Rough ER في جهاز جولجي؟',
     '23. Which face of the Golgi Apparatus receives transport vesicles from Rough ER?'),
    ('Cis face (الوجه غير الناضج)', 'Cis face (immature face)'),
    ('Trans face (الوجه الناضج)', 'Trans face (mature face)'),
    ('كلا الوجهين', 'Both faces'),
    ('لا يستقبل من rER', 'It does not receive from rER'),
    ('<b>Cis face</b> هو الوجه غير الناضج الذي يستقبل من rER. بينما <b>Trans face</b> هو منطقة الشحن التي ترسل الإفرازات والـ Lysosomes.',
     '<b>Cis face</b> is the immature face that receives from rER. The <b>Trans face</b> is the shipping area that sends secretory vesicles and Lysosomes.'),

    # Q24
    ('24. ماذا ينتج Trans face في جهاز جولجي؟',
     '24. What does the Trans face of the Golgi Apparatus produce?'),
    ('Transport vesicles فقط', 'Transport vesicles only'),
    ('Ribosomes فقط', 'Ribosomes only'),
    ('الـ <b>Trans face</b> ينتج: <b>Secretory vesicles للـ Exocytosis</b> و <b>Lysosomes</b>.',
     'The <b>Trans face</b> produces: <b>Secretory vesicles for Exocytosis</b> and <b>Lysosomes</b>.'),
]

for arabic, english in replacements:
    if arabic in content:
        content = content.replace(arabic, english)
        print(f'Replaced: {arabic[:50]}')
    else:
        print(f'NOT FOUND: {arabic[:60]}')

with open('lecture.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nDone. File saved.')
