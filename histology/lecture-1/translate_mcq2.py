import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('lecture.html', encoding='utf-8') as f:
    content = f.read()

# Fix remaining Arabic text in MCQ explanations and questions
fixes = [
    # Q15 question
    ('15. ما وظيفة Mitochondria؟', '15. What is the function of Mitochondria?'),
    # Q15 explain
    ('Mitochondria = <b>Powerhouses of living cells</b> تصنع ATP وهو المصدر الرئيسي للطاقة.',
     'Mitochondria = <b>Powerhouses of living cells</b>. They produce ATP, the main source of energy.'),
    # Q16 explain
    ('الغشاء الداخلي للميتوكوندريا يكوّن طيات تسمى <b>Cristae</b> وهي التي تزيد من المساحة السطحية لإنتاج الطاقة.',
     'The inner membrane of Mitochondria forms folds called <b>Cristae</b>, which increase the surface area for energy production.'),
    # Q17 question
    ('17. كم عدد الأغشية التي تحيط بالميتوكوندريا؟',
     '17. How many membranes surround Mitochondria?'),
    # Q17 explain
    ('الميتوكوندريا محاطة بـ <b>غشاءين (Double membranes)</b>: خارجي املس وداخلي يكوّن Cristae.',
     'Mitochondria are surrounded by <b>Double membranes</b>: a smooth outer membrane and an inner membrane forming Cristae.'),
    # Q18 question
    ('18. ماذا تحتوي مصفوفة الميتوكوندريا (Matrix)؟',
     '18. What does the Mitochondrial Matrix contain?'),
    # Q18 explain
    ('الـ Matrix تحتوي على: <b>Lipid, Protein, Carbohydrate, Ca, Mg, DNA, RNA, Oxidative enzymes</b> — ولاحظ ان الميتوكوندريا لديها DNA خاص بها!',
     'The Matrix contains: <b>Lipid, Protein, Carbohydrate, Ca, Mg, DNA, RNA, Oxidative enzymes</b> — note that Mitochondria have their own DNA!'),
    # Q1 explain (was missed due to already-replaced "حزمة الكترونات")
    ('الصواب: المجهر الإلكتروني يستخدم <b>Electron beam</b>، بينما المجهر الضوئي يستخدم الاشعة الضوئية.',
     'Correct: The Electron Microscope uses an <b>Electron beam</b>, while the Light Microscope uses light rays.'),
    # Q7 explain (was missed)
    ('<b>Glycogen</b> من الاحتواءات السيتوبلازمية (غير حي، مؤقت). Mitochondria وGolgi apparatus والLysosomes كلها عضيات.',
     '<b>Glycogen</b> is a cytoplasmic inclusion (non-living, temporary). Mitochondria, Golgi apparatus, and Lysosomes are all organelles.'),
    # Q22 question
    ('22. لماذا لا يظهر جهاز جولجي بصبغة H&amp;E؟',
     '22. Why is the Golgi Apparatus not stained by H&amp;E?'),
    # Q22 explain
    ('جهاز جولجي يذوب اثناء تحضير العينة بسبب <b>المحتوى الدهني العالي</b> في اغشيته، لذلك يظهر كمنطقة شاحبة = <b>Negative Golgi image</b>.',
     'Golgi Apparatus dissolves during specimen preparation due to its <b>high lipid content</b>, leaving a pale area called <b>Negative Golgi image</b>.'),
    # Q23 question
    ('23. ما الوجه الذي يستقبل حويصلات النقل من Rough ER في جهاز جولجي؟',
     '23. Which face of the Golgi Apparatus receives transport vesicles from Rough ER?'),
    # Q24 question
    ('24. ماذا ينتج Trans face في جهاز جولجي؟',
     '24. What does the Trans face of the Golgi Apparatus produce?'),
    # Q24 explain
    ('الـ <b>Trans face</b> ينتج: <b>Secretory vesicles للـ Exocytosis</b> و <b>Lysosomes</b>.',
     'The <b>Trans face</b> produces: <b>Secretory vesicles for Exocytosis</b> and <b>Lysosomes</b>.'),
    # Q9 missed option
    ('Ribosomes (Ribosomes)', 'Ribosomes'),
]

for arabic, english in fixes:
    if arabic in content:
        content = content.replace(arabic, english)
        print(f'OK: {arabic[:60]}')
    else:
        print(f'SKIP: {arabic[:60]}')

with open('lecture.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nDone.')
