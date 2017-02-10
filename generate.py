#2. Verificator, тип: generate. Структура и начальное заполнение базы данных
#!/usr/bin/env python
#coding: utf-8
#
# Программно-аппаратный комплекс "Автоматизация проведения поверочных процедур метрологического оборудования"
# (c) НПО "Химавтоматика", 2009 - 2011

# Структура и начальное заполнение базы данных

from elixir import *

def loadImageData (path):
    f = open(path,'rb')
    data = f.read()
    f.close()
    return data

# Структура БД

class DeviceType(Entity):
    using_options(tablename='de vice_types')
    id = Field(Integer, primary_key=True)
    model = Field(UnicodeText)
    description = Field(UnicodeText)
    type = Field(UnicodeText)
    check_interval = Field(Integer)
    documents = Field(UnicodeText)
    required_tools = ManyToMany('Tool')
    passport_parameters = ManyToMany('Parameter')
    question_groups = ManyToMany('QuestionGroup')

class Tool(Entity):
    using_options(tablename='tools')
    id = Field(Integer, primary_key=True)
    name = Field(UnicodeText)
    parameters = Field(UnicodeText)
    standarts = Field(UnicodeText)
    required_by = ManyToMany('DeviceType')

class Image(Entity):
    using_options(tablename='images')
    id = Field(Integer, primary_key=True)
    name = Field(UnicodeText)
    data = Field(LargeBinary)
    used_by = ManyToMany('Question')

class Question(Entity):
    using_options(tablename='questions')
    id = Field(Integer, primary_key=True)
    question_group = ManyToOne('QuestionGroup')
    num = Field(Integer)
    caption = Field(UnicodeText)
    text = Field(UnicodeText)
    images = ManyToMany('Image')
    condition = Field(UnicodeText)
    calculation = Field(UnicodeText)
    measurable_parameters = ManyToMany('Parameter')
    calculated_parameters = ManyToMany('Parameter')
    params = Field(UnicodeText)
    param_comments = Field(UnicodeText)
    param_names = Field(UnicodeText)
    param_hints = Field(UnicodeText)
    iterations = Field(Integer)
    question_type = ManyToOne('QuestionType')
    itercalc = Field(UnicodeText)
    itercond = Field(UnicodeText)
    iterparams = Field(UnicodeText)
    reportstring = Field(UnicodeText)
    conclusion_success = Field(UnicodeText)
    conclusion_failure = Field(UnicodeText)

class QuestionGroup(Entity):
    using_options(tablename='question_groups')
    id = Field(Integer, primary_key=True)
    caption = Field(UnicodeText)
    device_type = ManyToMany('DeviceType')
    num = Field(Integer)
    report_caption = Field(Boolean)
    questions = OneToMany('Question')

class QuestionType(Entity):
    using_options(tablename='question_types')
    id = Field(Integer, primary_key=True)
    typename = Field(UnicodeText)
    description = Field(UnicodeText)

class Unit(Entity):
    using_options(tablename = 'units')
    id = Field(Integer, primary_key = True)
    name = Field(UnicodeText)
    description = Field(UnicodeText)

class Parameter(Entity):
    using_options(tablename = 'parameters')
    id = Field(Integer, primary_key = True)
    variable_name = Field(UnicodeText)
    description = Field(UnicodeText)
    readable_name = Field(UnicodeText)
    hint = Field(UnicodeText)
    unit_name = ManyToOne('Unit')

# Начальное заполнение БД
if __name__ == '__main__':
    import sys
    import os
    from datetime import date

if hasattr(sys, 'frozen'):
    datapath = os.path.dirname(sys.executable)
elif __file__:
    datapath = os.path.dirname(__file__)
    datapath = os.path.join(datapath, 'verificator.db')
    dataconnstr = 'sqlite:///'+datapath
    metadata.bind = dataconnstr

setup_all()
create_all()

# Переменные
abs_percent = Unit(name = u'% абс.', description = u'Процент абсолютный')
celsius = Unit(name = u'°C', description = u'Градус Цельсия')
kilopascal = Unit(name = u'кПа', description = u'Килопаскаль')
rel_percent = Unit(name = u'%', description = u'Процент')
max_conc_lim = Unit(name = u'ПДК', description = u'Предельно допустимая концентрация')

K2 = Parameter(variable_name = u'K2',
                description = u'Погрешность воспроизведения коэффициента пропускания',
                readable_name = u'K<sub>2</sub>',
                hint = u'34',
                unit = abs_percent)
P23p = Parameter(variable_name = u'P23p',
                 description = u'Погрешность воспроизведения отн. разницы коэффициентов пропускания',
                 readable_name = u'П(23)<sub>П</sub>',
                 hint = u'9.35',
                 unit = abs_percent)
P24p = Parameter(variable_name = u'P24p',
                 description = u'Погрешность воспроизведения отн. разницы коэффициентов пропускания',
                 readable_name = u'П(24)<sub>П</sub>',
                 hint = u'4.75',
                 unit = abs_percent)
C2p = Parameter(variable_name = u'C2p',
                description = u'Эквивалентная концентрация на 1,5-2,5 ПДК для НОПС',
                readablename = u'C<sup>2</sup><sub>П</sub>',
                hint = u'2',
                unit = max_conc_lim)
C5p = Parameter(variable_name = u'C5p',
                description = u'Эквивалентная концентрация на 4-6 ПДК для НОПС',
                readable_name = u'C<sup>5</sup><sub>П</sub>',
                hint = u'5',
                unit = max_conc_lim)
C8p = Parameter(variable_name = u'C8p',
                description = u'Эквивалентная концентрация на 7-9 ПДК для НОПС',
                readable_name = u'C<sup>8</sup><sub>П</sub>',
                hint = u'8',
                unit = max_conc_lim)
DS0 = Parameter(variable_name = u'DS0',
                description = u'Предел допускаемой погрешности',
                readable_name = u'AS<sub>0</sub>',
                hint = u'0.25',
                unit = abs_percent)
ds0 = Parameter(variable_name = u'ds0',
                description = u'Предел CKO результата измерений',
                readable_name = u'S',
                hint = u'0.12',
                unit = rel_percent)
C1 = Parameter(variable_name = u'C1',
               description = u'Эквивалентная концентрация на 0,5-1,5 ПДК',
               readable_name = u'С1',
               hint = u'1',
               unit = max_conc_lim)
C2 = Parameter(variable_name = u'C2',
               description = u'Эквивалентная концентрация на 4-6 ПДК',
               readable_name = u'C2',
               hint = u'5',
               unit = max_conc_lim)
C3 = Parameter(variable_name = u'C3',
               description = u'Эквивалентная концентрация на 23-27 ПДК',
               readable_name = u'СЗ',
               hint = u'25',
               unit = max_conc_lim)
C4 = Parameter(variable_name = u'C4',
               description = u'Эквивалентная концентрация на 47-53 ПДК',
               readable_name = u'C4',
               hint = u'50',
               unit = max_conc_lim)
Ce1 = Parameter(variable_name = u'Ce1',
                description = u'Эквивалентная концентрация на 0,4-1 ПДК',
                readable_name = u'Ce1',
                hint=u'0.7',
                unit=max_conc_lim)
Ce2 = Parameter(variable_name=u'Ce2',
                description=u'Эквивалентная концентрация на 4-6 ПДК',
                readable_name=u'Ce2',
                hint=u'5',
                unit=max_conc_lim)
## Типы оборудования
# devtypel=DeviceType(model=u'Koмплект поверочный СНС-ИФГ для газоанализатора Яуза-М.01',
# description=u'Комплект поверочный СНС-ИФГ УТАМ5.940.000, предназначенный для '
# u'поэлементной поверки газоанализатора ЯУЗА-М.01',
# documents=u'5Б2.840.495 ДЛ1 - Методика поверки по сокращенной программе комплекта '
# u'поверочного СНС-ИФГ',
# check_interval=24, tуре=u'СНС-ИФГ',
# passport_parameters=[K2, Р23р, Р24р])
devtype2 = DeviceType(model=u'Прибор для измерения содержания воды ВАД-40М',
                      description=u'Прибор для измерения содержания воды ВАД-40М производства ООО НПФ '
                                  u'"Микроаналитические системы" и ООО НПФ "Технологическая аппаратура", г.'
                                  u'Санкт-Петербург',
                      documents=u'2302-0013-2007 МП - Методика поверки',
                      check_interval=12, tуре=u'ВАД-40М')
devtype3 = DeviceType(model=u'Измерительный преобразователь ДМК-21',
                      description=u'Измерительные преобразователи ДМК-21-Г, ДМК-21-А и ДМК-21-О',
                      documents=u'A2.840.000 ДЛ - Методика поверки',
                      check_interval=12, type=u'ДМK-21-Г, ДМК-21-А, ДМК-21-О',
                      passport_parameters=[C2p, C5p, C8p])
devtype4 = DeviceType(model=u'Газоанализатор ИГ-9',
                      description=u'Газoaнaлизатор ИГ-9 14-02.02.2.00.000, взрывозащищенный, предназначенный '
                                  u'для измерения концентрации горючих газов и сигнализации превышения их '
                                  u'концентраций установленного уровня во взрывоопасных зонах помещений '
                                  u'классов В-1, В-1а, В-1б и наружных установках класса В-1г, согласно гл. '
                                  u'7.3 ПУЭ',
                      documents=u'МП.MH 1363-2004 - Методика поверки; 14-02.02.2.00.000 РЭ -Руководство по эксплуатации',
                      check_interval = 6, type = u'ИГ-9')
devtype5 = DeviceType(model=u'Гaзoaнализатор ИКАР-Л.01',
                      description=u'Газоанализатор ИКАР-Л.01',
                      documents=u'MEKB.413411.002 ДЛ - Методика поверки; МЕКВ.413411.002 РЭ -Руководство по эксплуатации',
                      check_interval = 12, tуре = u'ИКАР-Л.01')


devtype6=DeviceType(model=u'Оптический спиртомер ИКОНЭТ-МП',
                    description=u'Спиртометры оптические типа "ИКОНЭТ-МП"',
                    documents=u'МГФК.414221.003 ПС - Паспорт; Методика поверки',
                    check_interval=12, type=u'ИКОНЕТ-МП',
                    passport_parameters=[DS0, ds0])
devtype7=DeviceType(model=u'Газоанализатор ИФГ-М',
                    description=u'Газоанализаторы типа ИФГ-М 5Б2.840.494',
                    documents=u'5Б2.840.494 ДЛ - Методика поверки; 5Б2.840.494 ПС - Паспорт; 5Б2.840.494 ТО -'
                              u'Техническое описание',
                    check_interval=12, tуре=u'ИФГ-М',
                    passport_parameters=[C1, C2, C3, C4])
devtype8=DeviceType(model=u'Счетчик оптико-электронный аэрозольный ОЭАС-05',
                    description=u'Счетчик оптико-электронный аэрозольный ОЭАС-05',
                    documents=u'9814.311.000MП - Методика поверки; 9814.311.000РЭ - Руководство по '
                              u'эксплуатации; 9814.311.000ПС - Паспорт',
                    check_interval=12, type=u'OЭAC-05')
devtype9=DeviceType(model=u'Газоанализатop инфракрасный ПГА-6',
                    description=u'Газоанализаторы инфракрасные ПГА всех исполнений, выпускаемые ОАО РНИИ'
                                u'"Электронстандарт", г. Санкт-Петербург',
                    documents=u'ЯВША.413311.000ПС - Паспорт',
                    check_interval=12, tуре=u'ПГА-6')
devtype10=DeviceType(model=u'Генератор влажного газа эталонный РОДНИК-6',
                     description=u'Генератор влажного газа эталонный РОДНИК-6 ТУ 4215-043-71803530-2007',
                     documents=u'5K1.550.153 ДП - Методика поверки',
                     check_interval=12, tуре=u'РОДНИК-6')
devtype11=DeviceType(model=u'Преобразователь температуры и влажности измерительный РОСА-10',
                     description=u'Преобразователи температуры и влажности измерительные РОСА-10',
                     documents=u'Методика поверки; НКГЖ414614.001РЭ - Руководство по эксплуатации',
                     check_interval=24, type=u'POCA-10')
devtype12=DeviceType(model=u'Газоанализатор СФГ-М.01',
                     description=u'Газоанализатор СФГ-М.01 MEKB.413322.005',
                     documents=u'MEKB.413322.005 ДЛ - Методика поверки; MEKB.413322.005 ФО -Формуляр; '
                               u'MEKB.413322.005 РЭ - Руководство по эксплуатации',
                     check_interval=12, tуре=u'СФГ-М.01',
                     passport_parameters=[Ce1, Ce2])
devtype13=DeviceType(model=u'Счетчик аэрозольных частиц',
                     description=u'Счетчик аэрозольных частиц, работающие в диапазоне измерения размеров'
                                 u'аэрозольных частиц от 0,3 до 30 мкм и в диапазоне счетных концентраций '
                                 u'от 0 до 10<sup>7</sup> дм<sup>-3 </sup>, предназначенные для контроля '
                                 u'запыленности воздуха различных производств, определения дисперсного '
                                 u'состава и счетной концентрации аэрозолей в соответствии с ГОСТ Р 8.606,'
                                 u'ГОСТ ИСО 14644-1.<br><u>Межповерочный интервал определяется'
                                 u'требованиями, изложенными в технической документации на конкретный тип '
                                 u'счетчика аэрозольных частиц.</u>',
                     documents=u'Методика поверки',
                     check_interval=0, type=u'')
devtype14 = DeviceType(model=u'Течеискатель-сигнализатор ФП 12',
                       description=u'Течеискатель-сигнализатор ФП 12, предназначенный для обнаружения утечек метана'
                                   u'(CH<sub>4</sub>), пропана (C<sub>3</sub>H<sub>8</sub>), или водорода (H<sub>2</ sub>)'
                                   u'и выдачи световой и звуковой сигнализации при превышении установленных пороговых'
                                   u'значений объемной доли газов.',
                       documents=u'Методика поверки',
                       check_interval=6, tуре=u'ФП 12')
devtype15 = DeviceType(model=u'Газоанализатор ФЛЮОРИТ-Ц',
                       description=u'Газоанализатор ФЛЮОРИТ-Ц, предназначенный для измерения объемной доли кислорода в'
                                   u'инертных газах и азоте, выпускаемый в соответствии с техническими условиями '
                                   u'5К1.552.045 ТУ',
                       documents=u'5K1.552.045 ДП - Инструкция по поверке; 5К1.552.045 РЭ -Руководство по эксплуатации;'
                                 u'5К0.283.000 ДА - Аттестат',
                       check_interval = 12, tуре = u'ФЛЮОРИТ-Ц')
devtype16 = DeviceType(model=u'Газоанализатор ЭССА',
                       description=u'Газоанализаторы ЭССА, предназначенные для измерения массовой концентрации оксида'
                                   u'углерода (СО), метана (CH<sub>4</sub>), сигнализации о превышении двух или трех'
                                   u'заданных уровней концентрации (ПОРОГ 1, ПОРОГ 2, ПОРОГ 3), и управления внешними'
                                   u'устройствами: исполнительными элементами систем вентиляции, звуковой и световой'
                                   u'сигнализации и др.',
                       documents=u'ЯPKГ 1.550.001-01РЭ - Руководство по эксплуатации; Приложение А к Руководству по '
                                 u'эксплуатации - Методика поверки',
                       check_interval=12, type=u'ЭCCA')
devtype17 = DeviceType(model=u'Барометр-анероид',
                       description=u'Мембранные барометры типа М-67 по ТУ 2504-1797-75, типа М-98 по ТУ 2511-1316-76,'
                                   u'типа БАММ-1 по ТУ 2511-1513-79 и типа М-110 по ТУ 2504-1799-75, предназначенные'
                                   u'для измерений давления в диапазоне от 0,7 до 109 кПа.<br><u>Межповерочный интервал для'
                                   u'барометров типов М-67 и М-98 - не более двух лет, для барометров типов БАММ-1 и М-110'
                                   u'- не более одного года.</u>',
                       documents=u'MИ 2705-2001 - Методика поверки',
                       check_interval=0, tуре=u'Барометр')
devtype18=DeviceType(model=u'Газоанализатор Яуза М.01',
                     description=u'Газоанализаторы типа Яуза-М.01 5Б2.840.494',
                     documents=u'5Б2.840.494 ДЛ - Методика поверки; 5Б2.840.494 ПС - Паспорт',
                     check_interval=12, type=u'Яуза-M.01',
                     passport_parameters=[C1, C2, C3, C4])
devtype19=DeviceType(model=u'Гигрометр Баргузин',
                     description=u'Гигрометр кулонометрический типа Баргузин',
                     documents=u'5K0.284.015 ДЛ - Методика поверки; 5К0.284.000 ТО - Инструкция по эксплуатации',
                     check_interval=24, tуре=u'Баргузин')
devtype20=DeviceType(model=u'Газоанализатор ФП 11.2к',
                     description=u'Газоанализатор ФП 11.2к',
                     documents=u'100162047.021-01 ПС - Паспорт',
                     check_interval=6, tуре=u'ФП 11.2к')
devtype21=DeviceType(model=u'Спиртометр МИ 138-77',
                     description=u'Спиртометр металлический рабочий МИ 138-77',
                     documents=u'Методика поверки',
                     check_interval=12, type=u'MИ 138-77')
devtype22=DeviceType(model=u'Генератор влажного газа РОДНИК-4',
                     description=u'Генератор влажного газа РОДНИК-4',
                     documents=u'5K2.844.100 ДП - Методика поверки',
                     check_interval=12, tуре=u'РОДНИК-4')
devtype23=DeviceType(model=u'Lighthouse Solair 5100',
                     description=u'Счетчик аэрозольных частиц лазерный Lighthouse модификации Solair 5100',
                     documents=u'МП № 242/1190-2010 - методика поверки',
                     check_interval=12, type=u'Solair 5100')
devtype24=DeviceType(model=u'Счетчик ПК ГТА-0.3-002',
                     description=u'Счетчик аэрозольных частиц ПК ГТА-0.3-002',
                     documents=u'МП № 242/1191-2010 - методика поверки',
                     check_interval=12, type=u'ПК ГТА-0.3-002')
devtype25=DeviceType(model=u'Lighthouse Remote 5010',
                     description=u'Счетчик аэрозольных частиц лазерный Lighthouse модификации Remote 5010',
                     documents=u'MП № 242/1192-2010 - методика поверки',
                     check_interval=12, type=u'Remote 5010')
devtype26=DeviceType(model=u'Счетчик ПКЗВ-906',
                     description=u'Счетчик аэрозольных частиц ПКЗВ-906',
                     documents=u'МП № 242/1193-2010 - методика поверки',
                     check_interval=12, type=u'ПКЗВ-906')
devtype27=DeviceType(model=u'Счетчик ОЭАС-05',
                     description=u'Счетчик аэрозольных частиц ОЭАС-05',
                     documents=u'МП № 242/1194-2010 - методика поверки',
                     check_interval= 12, type=u'OЭAC-05')

# Поверочное оборудование
#dt1_tool01=Тооl(name=u'Спектрофотометр СФ-18',
#parameters=u'Диапазоны измерений коэффициентов пропускания 1-100% и 90-110%, абсолютная погрешность'
#u'±0.5%, воспроизводимость ±0.3%', standarts=u'')
#dt1_tool02=Tool(name=u'Tepмометp ТЛ-4', parameters=u'Цена деления 0,1°С', standarts=u'ГOCT 28498-90')

dt1_tool03=Tool(name=u'Барометр-aнероид БАММ-1',
                parameters=u'Диапазон измерений давления 80-106кПа ±0.35кПа,'
                           u'цена деления 0,1 кПа',
                standarts=u'TУ 25-11.1513-79')

#dt1_tool04=Тool(name=u'Психрометр аспирационный МБ-4М',
#parameters=u'Диапазон измерений относительной влажности 10-100%', standarts=u'ГOCT 6353-52')

dt2_tool01=Tool(name=u'Цилиндp мерный', parameters=u'', standarts=u'ГOCT 1770')
dt2_tool02=Tool(name=u'Образец BH-0', parameters=u'Образец массовой доли воды в нефти, 0%', standarts=u'MИ 2590')
dt2_tool03=Tool(name=u'Образец ВН-1', parameters=u'Образец массовой доли воды в нефти, 1%', standarts=u'MИ 2590')
dt2_tool04=Tool(name=u'Образец ВН-3', parameters=u'Образец массовой доли воды в нефти, 3%', standarts=u'MИ 2590')
dt2_tool05=Tool(name=u'Образец ВН-6', parameters=u'Образец массовой доли воды в нефти, 6%', standarts=u'MИ 2590')
dt2_tool06=Tool(name=u'Термометр жидкостный стеклянный тип Б',
                parameters=u'Диапазон измерений 1-100°С, цена деления 0,1°С', standarts=u'ГOCT 28498-90')
dt2_tool07=Tool(name=u'Психрометр бытовой БП-1', parameters=u'', standarts=u'')
dt2_tool08=Tool(name=u'Барометр анероидный тип М-98', parameters=u'',
                standarts=u'ГОСТ 1793, ТУ 2511-1316-76')
dt3_tool01=Tool(name=u'ПЭBM', parameters=u'', standarts=u'')
dt3_tool02=Tool(name=u'Поверочное приспособление - НОПС', parameters=u'', standarts=u'A3.914.000 ТУ')
dt3_tool03=Tool(name=u'Пульт проверки ДМК-21', parameters=u'', standarts=u'A2.702.003')
dt3_tool04=Tool(name=u'Блок питания Б5-48', parameters=u'', standarts=u'EЭЗ.233.220 ТУ')
dt3_tool05=Tool(name=u'Кабели технологические', parameters=u'', standarts=u'')
dt3_tool06=Tool(name=u'Программа "Тест ДМК-21"', parameters=u'', standarts=u'')
dt3_tool07=Tool(name=u'Секундомер СОПр-2а-3 -3 кл', parameters=u'', standarts=u'ГOCT 5072-79')


#ГОСТ5072-79 заменен на ТУ 25-1894.003-90
dt3_tool08=Tool(name=u'Poтaмeтp РМ-А-0,063 ГУЗ', parameters=u'', standarts=u'ГOCT 13045-81')
dt4_tool01=Tool(name=u'Камера 14-93.3.00.00.006 для поверочной газовой смеси', parameters=u'', standarts=u'')
dt4_tool02=Tool(name=u'Poтaмeтp РМ-А-0,063', parameters=u'кл. 2,5', standarts=u'ГOCT 13045-76')
dt4_tool03=Tool(name=u'Poтaмeтp PM-A-0,063', parameters=u'кл. 4', standarts=u'ГOCT 13045-81')
dt4_tool04=Tool(name=u'ГCO состава смесей поверочных газовоздушных 2 разряда', parameters=u'',
                standarts=u'TУ РБ 100270876.079-2002')
dt4_tool05=Tool(name=u'смесь За’, parameters=u(1.00±0.16)%', standarts=u'CO РБ 07 0196 007')
dt4_tool06=Tool(name=u'cмecь 5а', parameters=u'(2.50±0.30)%', standarts=u'CO РБ 07 0198 00')
dt4_tool07=Tool(name=u'cмесь 3б', parameters=u'(0.40±0.08)%', standarts=u'CO РБ 07 0207 00')
dt4_tool08=Tool(name=u'cмecь 5б', parameters=u'(1.00±0.16)%', standarts=u'СО РБ 07 0209 00')
dt5_tool01=Tool(name=u'Бaллoн газовый с азотом газообразным техническим повышенной чистоты', parameters=u'',
                standarts=u'ГOCT 949-73, ГОСТ 9293-74')
dt5_tool02=Tool(name=u'Бaллoн газовый с ПГС (О2 в N2), ГСО 3726-87',
                parameters=u'O2=12± 1 об.д.(%)', standarts=u'TУ 6-16-2956-92')
dt5_tool03=Tool(name=u'Баллон газовый с ПГС (O2 в N2), ГСО 3730-87',
                parameters=u'O2=24±0,5 об.д.(%)', standarts=u'TУ 6-16-2956-92')
dt5_tool04=dt1_tool03
dt5_tool05=Tool(name=u'Tepмометр жидкостной стеклянный', parameters=u'Диапазон измерений от 0 до 100 °С, цена дел. 2 °С',
                standarts=u'ГOCT 28498-90')
dt6_tool01=Tool(name=u'Haбop эталонных стеклянных спиртомеров 1-го разряда',
                parameters=u'доверительная погрешность δ = 0,02 - 0,01%',
                standarts=u'ГOCT 8.024-75')
dt6_tool02=Tool(name=u'Tермометр', parameters=u'Диапазон измерения от 10°С до 50°С, цена деления не более 0,1 °С',
                standarts=u'ГOCT 13643-68')
dt7_tool01=Tool(name=u'Секундомер СОСпр-2а-3', parameters=u'Погрешность ±0,3 сек.', standarts=u'ГOCT 5072-79')
dt7_tool02=Tool(name=u'Poтaмeтp РМ-А-0,063 ГУЗ', parameters=u'', standarts=u'ГOCT 13045-81')
dt7_tool03=Tool(name=u'Koмплeкт СНС-ИФГ', parameters=u'Погрешность устанавливаемых величин эквивалентных концентраций ±1%',
                slandarts=u'УTAM5.940.000')
dt8_tool01=Tool(name=u'Paбочий эталон счетной концентрации аэрозольных частиц',
                parameters=u'Диапазон размеров частиц латекса 0,05-10,0 мкм, диапазон счетной концентрации частиц'
                           u'10-5*10^6 частиц/дмЗ, СКО 2,2%', standarts=u'Аттестован ГП ВНИИФТРИ св. №001-05-07')
dt8_tool02=Tool(name=u'Государственные стандартные образцы диаметра частиц типа М ОМИКС (ГСО 6015-91 ... 6038-91)',
                parameters=u'Haбop монодисперсных латексов со средним диаметром частиц 0,5; 5,0 мкм, 0,7-0.8; 6,0-8.0'
                           u'мкм. Дисперсия размера частиц 2-6 %', standarts=u'TУ 38.403.501-91')
dt8_tool03=Tool(name=u'Частотомер электронно-счетный Ч3-54', parameters=u'eЯ2.721.039ТУ',
                standarts=u'Интервалы времени t от 10 нс до 10^4 с. Амплитуда импульсов 10 мВ -100 В. Частота '
                          u'следования 0,1 Гц - 120 МГц. Погрешность измерений интервалов времени ± 1,5*10^-6*t')
dt8_tool04=Tool(name=u'Cчетчик газа барабанный РГ-7000', parameters=u'Объем 5,0 дм3. Класс точности 1,0',
standarts=u'TУ25.550 0039-80')
dt8_tool05=Tool(name=u'Бapoмeтp МД-49-2', parameters=u'TУ 2504.1618-72',
slandarts=u'Давление 76 - 107 кПа, кл. точности 1,0')
dt9_tool01=Tool(name=u'Tepмомeтp лабораторный ТЛ-4-А2', parameters=u'диапазон измерений (0 — 50) °С, цена деления 0,1 °С',
standarts=u'')
dt9_tool02=dt1_tool03
dt9_tool03=Tool(name=u'Психрометр аспирационный М-34', parameters=u'диапазон относительной влажности от 10 до 100% при '
                                                                  u'температуре от минус 10 до плюс 30 °С', standarts=u'TУ 25-1607.054-79')
dt9_tool04=Tool(name=u'Индикатор расхода - ротаметр РМ-А-0,063 УЗ', parameters=u'кл. 4',
                standarts=u'TУ25-02.070213082')
dt9_tool05=Tool(name=u'Beнтиль точной регулировки АПИ4.463.008', parameters=u'', standarts=u'')
dt9_tool06=Tool(name=u'Tpyбкa ПВХ', parameters=u'6 x 1,5', standarts=u'TУ 64-2-286-79')
dt9_tool07=Tool(name=u'Поверочные газовые смеси (ГСО-ПГС) метан - азот, пропан — азот, диоксид углерода — азот,'
                     u'кислород — азот в баллонах под давлением', parameters=u'', standarts=u'TУ 6-16-2956-92')
dt9_tool08=Tool(name=u'Поверочный нулевой газ (ПНГ) - воздух в баллонах под давлением', parameters=u'',
                standarts=u'TУ 6-21-5-821')
dt9_tool09=Tool(name=u'Поверочный нулевой газ (ПНГ) — азот в баллонах под давлением', parameters=u'',
                standarts=u'ГОСТ 9392-74')

dt10_tool01=Tool(name=u'Meгaoммeтp M1101M', parameters=u'Paбoчee напряжение 500 В; кт 1.0',
                 standarts=u'TУ25-04-800-71')
dt10_tool02=Tool(name=u'Кран-отсекатель', parameters=u'Paбoчee давление не менее 1 МПа, диаметр условного прохода не '
                                                     u'менее 1 мм', standarts=u'')
dt10_tool03=Tool(name=u'Бaллoн сжатого азота', parameters=u'Давленне от 0,5 до 15 МПа', standarts=u'')
dt10_tool04=Tool(name=u'Газосчетчик барабанный ГСБ-400', parameters=u'Диапазон измерений от 0,01 до 0,4 мЗ/ч; КТ 1.0',
                 standarts=u'')
dt10_tool05=Tool(name=u'Ceкyндомep', parameters=u'Диапазон измерений от 0 до 30 мин, точность хода ±0,4 с',
                 standarts=u'')
dt10_tool06=Tool(name=u'Гигрометр БАЙКАЛ-5Ц, откалиброванный в качестве компаратора по Государственному первичному '
                      u'эталону влажности', parameters=u'', standarts=u'')
dt10_tool07=Tool(name=u'Жидкий азот в сосудах Дьюара', parameters=u'', standarts=u'')
dt11_tool01 =Tool(name=u'Генератор влажного газа «Родник-2»',
                  parameters=u'Абсолютная погрешность воспроизведения относительной влажности ±0,5%', standarts=u'')
dt11_tool02=Tool(name=u'Генератор влажного газа «Родник-4»',
                 parameters=u'Абсолютная погрешность воспроизведения относительной влажности ±1,0%', standarts=u'')
dt11_tool03=Tool(name=u'Генератор влажного газа ГВГ-01',
                 parameters=u'Абсолютная погрешность воспроизведения относительной влажности ±1%. Абсолютная погрешность '
                            u'воспроизведения температуры точки росы ±1°С', standarts=u'')
dt11_tool04=Tool(name=u'Источник питания постоянного тока БП 96/24, БП 96/36',
                 parameters=u'Bыxoднoe напряжение: (24 ±0,48) В, (36 ±0,72) В. Ток нагрузки не более 45 мА',
                 standarts=u'TУ 4229-018-13282997-99')
dt11_tool05=Tool(name=u'Калибратор-измеритель унифицированных сигналов эталонный ИКСУ-2000',
                 parameters=u'Диапазон измерений тока: 0 ... 25 мА. Основная погрешность ±0,003 мА',
                 standarts=u'TУ 4381-031-13282997-00')
dt11_tool06=Tool(name=u'Калибратор температуры КТ-500',
                 parameters=u'Диапазон воспроизведения и измерения температуры от 50 до 500 °С',
                 standarts=u'TУ 4381-030-13282997-00')
dt11_tool07=Tool(name=u'Преобразователь давления измерительный АИР-20-ДА модель 040',
                 parameters=u'Диапазон 0 ÷ 160 кПа класс А (0,1 %)',
                 standarts=u'TУ 4212-032-13282997-02')
dt11_tool08=Tool(name=u'Эталонный барометр', parameters=u'', standarts=u'')
dt11_tool09=Tool(name=u'Термометр сопротивления платиновый вибропрочный эталонный ПТСВ-3 3-го разряда',
                 parameters=u'Диапазон минус 50 .. +500 °С. Основная погрешность не более 0,07 °С',
                 standarts=u'TУ 4211-041-13282997-02')
dt11_tool10=Tool(name=u'Жидкостный термостат U15C ТТЛ 32386',
                 parameters=u'Диапазон минус 60 .. +260 °С Погрешность термостатирования не более 0,02 °С',
                 standarts=u'')
dt11_tool11 =Tool(name=u'Мегаомметр Ф4102/1',
                  parameters=u'Диапазон измерений 0 .. 10000 МОм, U = 500 В Предел допускаемой основной погрешности ±1,5%',
                  standarts=u'TУ25-75340005-87')
dt12_tool01=Tool(name=u'Ротаметр РМ-А-0,1 ГУЗ',
                 parameters=u'Диапазон измерения расхода от 0 до 100 л/ч. Пределы допускаемой относительной погрешности'
                            u'измерений расхода ± 1,0 %', standarts=u'TУ1-01-0249-75')
dt12_tool02=Tool(name=u'Комплекс газоаналитический поверочный РЭКРТ',
                 parameters=u'Диалазон воспроизводимых концентраций от 0,1 до 50 ПДКР.З., пределы допускаемой'
                            u'относительной суммарной погрешности воспроизводимых значений концентраций продуктов'
                            u'NO2, НДМГ, ММГ-±10%, продукта N2H4-± 15 %',
                 standarts=u'cepтификат RU.E.31.081.А № 14051, Госреестр № 24289-03')
dt12_tool03=Tool(name=u'Тepмомeтp жидкостный стеклянный',
                 parameters=u'Диапазон измерений температуры от минус 50 до 50 °С, цена деления 0,1 °С',
                 standarts=u'ГOCT 28498-90')
dt12_tool04=Tool(name=u'Бapoмeтp-aнepoид метеорологический БАММ-1',
                 parameters=u'Диапазон измерений от 610 до 790 мм. рт. ст., предел допускаемой основной погрешности '
                            u'измерений 2,5 мм. рт. ст.', standarts=u'TУ25-11.1513-79')
dt12_tool05=Tool(name=u'Гигрометр «Волна-5»', parameters=u'Диапазон измерений относительной влажности от 0 до 100 %',
                 standarts=u'ГOCT 23382-78')
dt12_tool06=Tool(name=u'Tpyбкa фторопластовая Ф-4Мб', parameters=u'5,0 х 0,55 -15 м',
                 standarts=u'TУ6-05-041-510-82')
dt12_tool07=Tool(name=u'Тройник стеклянный', parameters=u'', standarts=u'5Б7.352.168')
dt12_tool08=Tool(name=u'Секундомер механический СОСпр-2а-3', parameters=u'Шкала 0-60 с. Цена деления 0,2 с',
                 standarts=u'TУ25-02.1894.003-90')
dt12_tool09=Tool(name=u'Комплект поверочный СНС-ИФГ',
                 parameters=u'Пределы допускаемой погрешности воспроизведения эквивалентных концентраций ± 1 %',
                 standarts=u'УTАМ5.940.000 ТУ')
dt12_tool10=Tool(name=u'Сетевой адаптер БПН 12.0-1.0', parameters=u'Hoминальное напряжение - 12 В, ток 1 А',
                 standarts=u'')
dt12_tool11 =Tool(name=u'Кабель K1', parameters=u'Обecпeчивaeт связь сетевого адаптера с газоанализатором.',
                  standarts=u'MEKB.658611.159')
dt13_tool01=Tool(name=u'Гeнepaтop аэрозолей АГ-1',
                 parameters=u'Производительность - не менее 45 дмЗ/мин. Обеспечивать генерирование монодисперсных или '
                            u'полидисперсных аэрозолей в диапазоне размеров 0.25 ... 30 мкм, и в диапазоне счетной концентрации от '
                            u'10 до 10^7 /дм3', standarts=u'')
dt13_tool02=Tool(name=u'Haбop суспензий монодисперсных или полидисперсных латексов, или порошкообразных материалов',
                 parameters=u'Диаметры частиц в диапазоне размеров 0.25 ... 30 мкм с погрешностью воспроизведения'
                            u'размера не более ± (2 ... 4) %. Полидисперсные наборы рекомендуется использовать при поверке приборов '
                            u'с нормируемыми параметрами в широком диапазоне размеров', standarts=u'')
dt13_tool03=Tool(name=u'Рабочий эталон для измерения счетной концентрации аэрозолей - Счетчик или совокупность счетчиков'
                      u'частиц аэрозолей в ранге рабочего эталона',
                 parameters=u'Диапазон измерения размеров частиц (0.3 ... 30) мкм. Диапазон измерения счетной'
                            u'концентрации - (100 ... 10^6)/дм3. Погрешность измерения счетной концентрации аэрозолей '
                            u'в заданных диапазонах размеров частиц не более ±(5 ... 8) %', standarts=u'')
dt13_tool04=Tool(name=u'Tройник', parameters=u'', standarts=u'')
dt13_tool05=Tool(name=u'Секундомер СОПпр-2а-2-010', parameters=u'Погрешность измерения интервала времени не более ± 0.1 с',
                 standarts=u'')
dt13_tool06=Tool(name=u'Pacxoдомеpы - счетчики газа РГС-1, РГС-2',
                 parameters=u'Диапазон измерения расхода - (0.2 ... 25) дмЗ/мин. Относительная погрешность измерения'
                            u'не более ±1,5 %', standarts=u'')
dt13_tool07=Tool(name=u'Измеритель температуры и влажности ИТВ 1522D',
                 parameters=u'Oтносительная погрешность измерения температуры не более ± 0,5 %. Относительная'
                            u'погрешность измерения влажности не более ± 2 %', standarts=u'')
dt13_tool08=Tool(name=u'Бapoмeтp - анероид БАММ-1', parameters=u'Oтносительная погрешность измерения не более ± 1 %',
                 standarts=u'')
dt13_tool09=Tool(name=u'Мини-компрессор SECOH', parameters=u'Производительность до 310 дмЗ/мин', standarts=u'')
dt13_tool10=Tool(name=u'Стабилизатор давления СДВ-25',
                 parameters=u'Maксимальное отклонение выходного давления не более ± 0,02 кПа', standarts=u'')
dt13_tool11=Tool(name=u'Фильтр очистки воздуха ФВ-25', parameters=u'Cтeпeнь очистки воздуха, не менее: 99,95%',
                 standarts=u'')
dt14_tool01=Tool(name=u'ГCO - ПГС СН4 - воздух, С3Н8 - воздух, Н2 - воздух в баллонах под давлением', parameters=u'',
                 standarts=u'TУ 6-16-2956-92')
dt14_tool02=Tool(name=u'Секундомер СОС Пр-2-2', parameters=u'кл. 3', standarts=u'TУ 25-1894.003-90')
dt14_tool03=Tool(name=u'Poтaмeтp РМ-А-0,063Г УЗ', parameters=u'0-0,63 м3/ч', standarts=u'ГOCT 13045-61')
dt14_tool04=Tool(name=u'Beнтиль точной регулировки BTP', parameters=u'', standarts=u'АПИ4.463.002')
dt14_tool05=Tool(name=u'Tpyбкa поливинилхлоридная (ПВХ)', parameters=u'6 x 15', standarts=u'TУ 64-2-286-79')
dt15_tool01=Tool(name=u'Maномeтp', parameters=u'0 — 100 кПа, Кл. 0,4', standarts=u'')
dt15_tool02=Tool(name=u'Источник сжатого газа (воздух, азот, аргон) с давлением не менее 60 кПа', parameters=u'',
                 standarts=u'')
dt15_tool03=Tool(name=u'Ceкундомep', parameters=u'Kл. 3', standarts=u'')
dt15_tool04=Tool(name=u'Вентиль запорный', parameters=u'условный проход DУ = 2 мм, 0—100 кПа', standarts=u'')
dt15_tool05=Tool(name=u'Мегаомметр M1102', parameters=u'500B, 500 МОм, Кл. 1', standarts=u'TУ 25-04-800-71')
dt15_tool06=Tool(name=u'Поверочные газовые смеси (в дальнейшем ПГС) кислород — азот', parameters=u'',
                 standarts=u'TУ 6-16-2956-92')
dt15_tool07=Tool(name=u'Поверочные газовые смеси (ПГС) с объемной долей кислорода (5,0 ± 2,0)%, (15,0 В 5,0) %',
                 parameters=u'', standarts=u'')
dt15_tool08=Tool(name=u'Kpaн механический поворотный КМП4М-422', parameters=u'', standarts=u'TУ 6-83.5Е4.460.130 ТУ')
dt15_tool09=Tool(name=u'Регистрирующий прибор РП-160', parameters=u'', standarts=u'ГOCT 7164-78')
dt16_tool01=Tool(name=u'Meгaoммeтp МА 100/4', parameters=u'c рабочим напряжением 500 В, кл. 3,5', standarts=u'')
dt16_tool02=Tool(name=u'Установка УПУ-1М', parameters=u'', standarts=u'У3.771.001ТУ')
dt16_tool03=Tool(name=u'Генератор газовых смесей ГТС-03-03 в комплекте с ГСО-ПГС CO/N2 в баллонах под давлением',
                 parameters=u'пределы допускаемой относительной погрешности Д0 = ± (4 - 7)%',
                 standarts=u'ШДЕK.418313.001 ТУ, ТУ 6-16-2956-92')
dt16_tool04=Tool(name=u'ГCO-ПГC СН4 в воздухе в баллонах под давлением',
                 parameters=u'пределы допускаемой относительной погрешности Д0 = ± (0,5 - 4)%',
                 standarts=u'TУ 6-16-2956-92')
dt16_tool05=Tool(name=u'Установка УПГС-01Х', parameters=u'пределы допускаемой относительной погрешности ДО = ± 7%',
                 standarts=u'АБЛК.468784.400 ТУ')
dt16_tool06=Tool(name=u'Баллон с нулевым воздухом - ПНГ', parameters=u'', standarts=u'TУ 6-21-5-82')
dt16_tool07=Tool(name=u'Poтaмeтp PM 064', parameters=u'Кл. 1', standarts=u'TУ 9907')
dt16_tool08=Tool(name=u'Тройник стеклянный', parameters=u'', standarts=u'ГOCT 9964')
dt16_tool09=Tool(name=u'Трубка Ф4-МБ', parameters=u'6,0 x 1,0 мм', standarts=u'TУ 6-05-041-760-85')
dt16_tool10=Tool(name=u'Термометр лабораторный ТЛ 4-A2',
                 parameters=u'диапазон измерения -50 ÷ +50 °C , цена деления 0,1 °С', standarts=u'ГOCT 28498')
dt16_tool11=Tool(name=u'Психрометр аспирационный M34', parameters=u'диапазон измерений относительной влажности 10 — 100%',
                 standarts=u'TУ 25-1607.054-85')
dt17_tool01=Tool(name=u'Бapoмeтp эталонный БОП-1 (БРС-1М-3) + ППК-1', parameters=u'4 - 1100 гПа, ±0,1 гПа (±0,2 гПа)',
                 standarts=u'6Г2.832.031 ТУ')
dt17_tool02=Tool(name=u'Maномeтp эталонный 1-го разряда МПА-15', parameters=u'погрешность не более 0,25 гПа',
                 standarts=u'TУ 50.62-83')
dt17_tool03=Tool(name=u'Teрмомeтp стеклянный', parameters=u'-20-+50 °С, ±0,2 °С', standarts=u'ГOCT 112-78')
dt17_tool04=Tool(name=u'Измеритель влажности ИВА-6АР', parameters=u'10% -95%, погрешность не более 3%',
                 standarts=u'')
dt17_tool05=Tool(name=u'Секундомер СОПпр-2а-011', parameters=u'', standarts=u'TУ 25-1819.0021-90')
dt18_tool01=Tool(name=u'Секндомер СОПпр-2а-3', parameters=u'погрешность ±0,3 сек.', standarts=u'ГOCT 5072-79')
dt18_tool02=Tool(name=u'Ротаметр РМД-0,063 ГУЗ', parameters=u'', standarts=u'ГOCT 13045-81')
dt18_tool03=Tool(name=u'Koмплeкт поверочный СНС-ИФГ', parameters=u'Предел основной относительной погрешности ±12%',
                 standarts=u'УТAM5.940.000 ТУ')
dt18_tool04=Tool(name=u'Образцовый комплекс ОЛИК-ФИАЛКА-О (на продукт О)', parameters=u'Диапазон 0,05-200 мг/мЗ, Погрешность ±6%', standarts=u'5B1.550.290-01TУ №1')
dt18_tool05=Tool(name=u'Образцовый комплекс ОЛИК-ФИАЛКА-А (на продукт A)', parameters=u'Диапазон 0,05-5 мг/м3, Погрешность ±7,5%', standarts=u'5B1.550.290-01 ТУ №2')
dt18_tool06=Tool(name=u'Образцовый комплекс ОЛИК-ФИАЛКА-Г (на продукт Г)', parameters=u'Диапазон 0,05-5 мг/мЗ, Погрешность ±5,6%', standarts=u'5B1.550.290 ТУ №2')
dt18_tool07=Tool(name=u'Образцовый комплекс ОЛИК-ФИАЛКА-Г (на продукт ММГ)', parameters=u'Диапазон 0,05-5 мг/мЗ, Погрешность ±5,6%', standarts=u'5B1.550.290 ТУ №2')

dt19_tool01=Tool(name=u'Мегаомметр постоянного тока M1101/3', parameters=u'', standarts=u'ТУ 2504-2130-72')
dt19_tool02=Tool(name=u'Манометр образцовый МО, кл. 4', parameters=u'0-400 кПа', standarts=u'')
dt19_tool03=Tool(name=u'Мост постоянного тока МО-62, кл. 1', parameters=u'0-2000 мкОм', standarts=u'')
dt19_tool04=Tool(name=u'Вентиль запорный 10Э6', parameters=u'', standarts=u'TУ 6-80 5Г4.463.013ТУ')
dt19_tool05=Tool(name=u'Секндомер, кл. 3', parameters=u'0-60 с, 0-30 мин', standarts=u'ГОСТ 5072-79')
dt19_tool06=Tool(name=u'Редуктор ДКП-1-65', parameters=u'', standarts=u'TУ 26-05-463-76')
dt19_tool07=Tool(name=u'Термометр', parameters=u'диапазон измерений 0-50 °C, цена деления 0,1 °C', standarts=u'')
dt19_tool08=Tool(name=u'Комбинированный прибор Ц4341, кл. 2,5', parameters=u'', standarts=u'TУ 25-04-3300-71')
dt19_tool09=Tool(name=u'Барометр-aнероид', parameters=u'80-104,5 кПа', standarts=u'TУ 25-04-1618-72')
dt19_tool10=Tool(name=u'Потенциометр самопишущий, кл. 0,25', parameters=u'0-10 мВ', standarts=u'')
dt19_tool11=Tool(name=u'Миллиамперметр самопишущий, кл. 0,25', parameters=u'0-5 мА', standarts=u'')
dt19_tool12=Tool(name=u'Вакуумметр ВО, кл. 0,4', parameters=u'-100-0 кПа', standarts=u'')
dt19_tool13=Tool(name=u'Побудитель ПЭП-3-4015', parameters=u'', standarts=u'TУ 6-83 АМЩ2.505.004 ТУ')
dt19_tool14=Tool(name=u'Азот газообразный', parameters=u'1 баллон', standarts=u'ГОСТ 9293-74')
dt19_tool15=Tool(name=u'Воздух', parameters=u'1 баллон', standarts=u'ГОСТ 24484-80, OCT 92-1577-78')
dt19_tool16=Tool(name=u'Генератор влажного газа Родник-6', parameters=u'', standarts=u'TУ 4215-043-71803530-2007')
dt20_tool01=Tool(name=u'Баллоны стальные', parameters=u'Eмкость (2-40)*10^-3 м3', standarts=u'ГОСТ 949')
dt20_tool02=Tool(name=u'Редуктор кислородный БКО-50-2', parameters=u'0-20 МПа', standarts=u'ГОСТ 13861')
dt20_tool03=Tool(name=u'Вентиль точной регулировки BTP', parameters=u'0-2,16*10^-3 мЗ/с', standarts=u'АПИ4.463.002')
dt20_tool04=Tool(name=u'Трубка (тройник) TC-T-6', parameters=u'', standarts=u'ГОСТ 25336')
dt20_tool05=Tool(name=u'Шланг соединительный полихлорвиниловый ПВХ-3,5x0,8', parameters=u'диаметр 3,5 мм (внутренний)', standarts=u'TУ 64-05838972-5')
dt20_tool06=Tool(name=u'Ротаметр РМ-А-0,063Г', parameters=u'0-0,063м3/ч', standarts=u'ГОСТ 13045')
dt20_tool07=Tool(name=u'Секундомер COC Пр-2-2', parameters=u'0-60 мин', standarts=u'')
dt20_tool08=Tool(name=u'Гигрометр психрометрический ВИТ-1', parameters=u'0-25 градус', standarts=u'')
dt20_tool09=Tool(name=u'Барометр анероид БАММ-1', parameters=u'75-106,5 кПа', standarts=u'ГОСТ')
dt21_tool01=Tool(name=u'образцовый металлический спиртомер 2-го разряда', parameters=u'', standarts=u'ГОСТ 3638-53')
dt21_tool02=Tool(name=u'спиртомер металлический рабочий', parameters=u'', standarts=u'ГОСТ 3638-53')
dt21_tool03=Tool(name=u'Набор ареометров для спирта исполнения БС1', parameters=u'', standarts=u'ГОСТ 3637-73')
dt21_tool04=Tool(name=u'цилиндры стеклянные', parameters=u'диаметром 50 мм и высотой 335 мм', standarts=u'ГОСТ 9545-73')
dt21_tool05=Tool(name=u'цилиндры стеклянные', parameters=u'диаметром 67 мм и высотой 335 мм', standarts=u'ГОСТ 9545-73')
dt21_tool06=Tool(name=u'цилиндры стеклянные', parameters=u'диаметром 90 мм и высотой 415 мм', standarts=u'ГОСТ 9545-73')
dt21_tool07=Tool(name=u'цилиндры стеклянные', parameters=u'диаметром 120 мм и высотой 520 мм', standarts=u'ГОСТ 9545-73')
dt21_tool08=Tool(name=u'цилиндры измерительные исполнения 1', parameters=u'вместимостью 500 мл', standarts=u'ГОСТ 1770-74')
dt21_tool09=Tool(name=u'цилиндры измерительные исполнения 1', parameters=u'вместимостью 1000 мл', standarts=u'ГОСТ 1770-74')
dt21_tool10=Tool(name=u'цилиндры измерительные исполнения 1', parameters=u'вместимостью 2000 мл', standarts=u'ГОСТ 1770-74')
dt21_tool11=Tool(name=u'дистиллятор типа Д-1', parameters=u'', standarts=u'')
dt21_tool12=Tool(name=u'лупа ЛП1-2,5х', parameters=u'', standarts=u'ГОСТ 7594-75')
dt21_tool13=Tool(name=u'мензурки ', parameters=u'вместимостью 50 мл', standarts=u'ГОСТ 1770-74')
dt21_tool14=Tool(name=u'мензурки ', parameters=u'вместимостью 1000 мл', standarts=u'ГОСТ 1770-74')
dt21_tool15=Tool(name=u'воронка ВФ 60-ПОР160-36', parameters=u'', standarts=u'ГОСТ 9775-69')
dt21_tool16=Tool(name=u'стеклянные бутылu', parameters=u'вместимостыо 10000 мл (с притертыми пробками)',
                 standarts=u'ГОСТ 14182-69')
dt21_tool17=Tool(name=u'воронка В75-140 ХУ-1', parameters=u'', standarts=u'ГОСТ 8613-75')
dt21_tool18=Tool(name=u'секундомер СОП нпр-6а-2', parameters=u'', standarts=u'ГОСТ 5072-72')
dt21_tool19=Tool(name=u'стекла покровные', parameters=u'диаметрами 110, 140, 190,240,260 мм', standarts=u'')
dt21_tool20=Tool(name=u'бумага фильтровальная лабораторная марки ФО', parameters=u'', standarts=u'ГОСТ 5636-70')
dt21_tool21=Tool(name=u'полотенца льняные', parameters=u'', standarts=u'ГОСТ 10232-68')
dt21_tool22=Tool(name=u'установка для поверки ареометров', parameters=u'', standarts=u'')
dt21_tool23=Tool(name=u'термостат типа TC-24 или ТС-32', parameters=u'', standarts=u'')
dt21_tool24=Tool(name=u'термометр типа ТПК № 11-П-200', parameters=u'', standarts=u'ГОСТ 9871-75')
dt21_tool25=Tool(name=u'приспособление деревянное с гнездами для сушки металлических, стеклянных спиртомеров и гирек', parameters=u'', standarts=u'')
dt21_tool26=Tool(name=u'психрометр аспирационный', parameters=u'', standarts=u'ГОСТ 6353-52')
dt21_tool27=Tool(name=u'барометр «Анероид»', parameters=u'', standarts=u'')
dt21_tool28=Tool(name=u'термометр 4-A - 2', parameters=u'', standarts=u'ГОСТ 215-73')
dt21_tool29=Tool(name=u'электроплитка ЭП4-1-1/220', parameters=u'', standarts=u'ГОСТ 306-76')
dt21_tool30=Tool(name=u'стаканы стеклянные с носикамu', parameters=u'вместимостью 100, 250 и 1000 мл', standarts=u'ГОСТ 10394-72')
dt21_tool31=Tool(name=u'штaнгeнциpкyль', parameters=u'c пределами измерения 0 -200, погрешность измерения 0,05',
                 standarts=u'ГОСТ 166-73')
dt21_tool32=Tool(name=u'люксметр типа Ю-16', parameters=u'c пределами измерения 0 - 500 лк', standarts=u'')
dt21_tool33=Tool(name=u'промывочные жидкостu', parameters=u'', standarts=u'')
dt21_tool34=Tool(name=u'спирт этиловый ректификованный', parameters=u'', standarts=u'ГОСТ 5962-67')
dt21_tool35=Tool(name=u'вода дистиллированная однократной перегонкu', parameters=u'', standarts=u'')
dt21_tool36=Tool(name=u'серная кислота ХЧ', parameters=u'', standarts=u'ГОСТ 4204-77')
dt21_tool37=Tool(name=u'хромовая смесь (смесь 60 г двухромовокислого калия по ГОСТ 2652-71, 1 л дистиллированной воды и 1 л серной кислоты ХЧ по ГОСТ 4204-77 плотностью 1840 кг/мЗ)', parameters=u'', standarts=u'')
dt22_tool01=Tool(name=u'Термометры ТЛ-4 №2 и №3', parameters=u'ЦД 0,1 °С', standarts=u'TУ 25-2021-003-88')
dt22_tool02=Tool(name=u'Контрольный гигрометр-компаратор БАЙКАЛ-5Ц', parameters=u'', standarts=u'5K1.550.130 ТУ')
dt23_tool01=Tool(name=u'Счетчик аэрозольных частиц Solair 3100+', parameters=u'пределы допускаемой относительной погрешности ±8,0%', standarts=u'(зав. № 100804002)')
dt23_tool02=Tool(name=u'Гeнepaтop аэрозоля ATM 226', parameters=u'', standarts=u'')
dt23_tool03=Tool(name=u'Ocyшитeль воздуха DDU 570/H', parameters=u'', standarts=u'')
dt23_tool04=Tool(name=u'Стандартные образцы гранулометрического состава на основе монодисперсных полистирольных латексов: ОГС-05ЛМ, ОГС-07ЛМ; ОГС-08ЛМ; ОГС-09ЛМ', parameters=u'границы относительной погрешности аттестованного значения (Р=0,95) ±5%', standarts=u'')
dt23_tool05=Tool(name=u'Камера смесительная аэрозольная КСА-1', parameters=u'', standarts=u'ШДЕК.418313.001')
dt23_tool06=Tool(name=u'Расходомер-cчетчик газа Delta G16', parameters=u'пределы допускаемой относительной погрешности ±1,0%', standarts=u'')
dt23_tool07=Tool(name=u'Управляющий вычислительный комплекс УВК-О1', parameters=u'', standarts=u'ШДЕК.421415.001')
dt23_tool08=Tool(name=u'Лабораторная посуда', parameters=u'класс точности не ниже 2', standarts=u'')
dt23_tool09=Tool(name=u'Прибор для контроля параметров микроклимата Testo  622', parameters=u'абсолютные погрешности измерений: температура,°С: ±0,4+1 мл.разр.; влажность (при 25 °С),%: ±2+1 мл.разр.; абсолютное давление,гПа: ±3+1 мл.разр.', standarts=u'')
dt23_tool10=Tool(name=u'Вода дистиллированная', parameters=u'', standarts=u'ГOCT 6709-72')
dt24_tool01=Tool(name=u'Счетчик аэрозольных частиц Solair 3100+', parameters=u'пределы допускаемой относительной погрешности ±8,0%', standarts=u'(зав. № 100804002)')
dt24_tool02=Tool(name=u'Разбавитель аэрозоля DIL 554', parameters=u'', standarts=u'')
dt24_tool03=Tool(name=u'Генератор аэрозоля ATM 226', parameters=u'', standarts=u'')
dt24_tool04=Tool(name=u'Осушитель воздуха DDU 570/H', parameters=u'', standarts=u'')
dt24_tool05=Tool(name=u'Камера смесительная аэрозольная КСА-1', parameters=u'', standarts=u'ШДЕK.418313.001')
dt24_tool06=Tool(name=u'Стандартные образцы гранулометрического состава на основе монодисперсных полистирольных латексов: ОГС-02ЛМ, ОГС-О3ЛМ, ОГС-04ЛМ, ОГС-06ЛМ, ОГС-07ЛМ', parameters=u'границы относительной погрешности аттестованного значения (Р=0,95) ±5%', standarts=u'')
dt24_tool07=Tool(name=u'Расходомер-счетчик газа РГС-1', parameters=u'пределы допускаемой относительной погрешности ±1,0%', standarts=u'ШДЕК.421322.001')
dt24_tool08=Tool(name=u'Управляющий вычислительный комплекс УВК-01', раrаmеters=u'', standarts=u'ШДEK.421415.001')
dt24_tool09=Tool(name=u'Лабораторная посуда', parameters=u'класс точности не ниже 2', standarts=u'')
dt24_tool10=Tool(name=u'Прибор для контроля параметров микроклимата Testo 622', parameters=u'абсолютные погрешности измерений: температура,°С: ±0,4+1 мл.разр.; влажность (при 25 °С),%: ±2+1 мл.разр.; абсолютное давление,гПа: ±3+1 мл.разр.', standarts=u'')
dt24_tool11=Tool(name=u'Секундомер СОПпр-2а-2-010', parameters=u'пределы допускаемой абсолютной погрешности ±0,1 с', standarts=u'')
dt24_tool12=Tool(name=u'Вода дистиллированная', parameters=u'', standarts=u'ГOCT 6709-72')
dt25_tool01=Tool(name=u'Счетчик аэрозольных частиц Solair 3100+', parameters=u'пределы допускаемой относительной погрешности ±8,0%', standarts=u'(зав. № 100804002)')
dt25_tool02=Tool(name=u'Генератор аэрозоля ATM 226', parameters=u'', standarts=u'')
dt25_tool03=Tool(name=u'Осушитель воздуха DDU 570/H', parameters=u'', standarts=u'')
dt25_tool04=Tool(name=u'Стандартные образцы гранулометрического состава на основе монодисперсных полистирольных латексов: ОГС-05ЛМ, ОГС-09ЛМ', parameters=u'границы относительной погрешности аттестованного значения (Р=0,95) ±5%', standarts=u'')
dt25_tool05=Tool(name=u'Разбавитель тестового аэрозоля DIL 554', parameters=u'', standarts=u'')
dt25_tool06=Tool(name=u'Kaмepa смесительная аэрозольная КСА-1', parameters=u'', standarts=u'ШДEK.418313.001')
dt25_tool07=Tool(name=u'Pacxoдомеp-cчетчик газа РГС-2', parameters=u'пределы допускаемой относительной погрешности ±1,0%', standarts=u'(3aв. № 307)')
dt25_tool08=Tool(name=u'Управляющий вычислительный комплекс УВК-01', parameters=u'', standarts=u'ШДЕК.421415.001')
dt25_tool09=Tool(name=u'Лабораторная посуда', parameters=u'класс точности не ниже 2', standarts=u'')
dt25_tool10=Tool(name=u'Прибор для контроля параметров микроклимата Testo 622', parameters=u'абсолютные погрешности измерений: температура,°С: ±0,4+1 мл.разр.; влажность (при 25 °С),%: ±2+1 мл.разр.; абсолютное давление,гПа: ±3+1 мл.разр.', standarts=u'')
dt25_tool11=Tool(neme=u'Вода дистиллированная', parameters=u'', standarts=u'ГOCT 6709-72')
dt26_tool01=Tool(name=u'Счетчик аэрозольных частиц Solair 3100+', parameters=u'пределы допускаемой относительной погрешности ±8,0%', standarts=u'(зaв. № 100804002)')
dt26_tool02=Tool(name=u'Разбавитель аэрозоля DIL 554', parameters=u'', standarts=u'')
dt26_tool03=Tool(name=u'Генератор аэрозоля ATM 226', parameters=u'', standarts=u'')
dt26_tool04=Tool(name=u'Ocyшитель воздуха DDU 570/H', parameters=u'', standarts=u'')
dt26_tool05=Tool(name=u'Kaмepa смесительная аэрозольная КСА-1', parameters=u'', standarts=u'ШДEK.418313.001')
dt26_tool06=Tool(name=u'Cтaндapтныe образцы гранулометрического состава на основе монодисперсных полистирольных латексов: ОГС-02ЛМ, ОГС-04ЛМ, ОГС-07ЛМ, ОГС-08ЛМ, ОГС-09ЛМ', parameters=u'границы относительной погрешности аттестованного значения (Р=0,95) ±5%', standarts=u'')
dt26_tool07=Tool(name=u'Расходомер-счтчик газа РГС-1', parameters=u'пределы допускаемой относительной погрешности ±1,0%', standarts=u'ШДЕK.421322.001')
dt26_tool08=Tool(name=u'Управляющий вычислительный комплекс УВК-01', parameters=u'', standarts=u'ШДEK.421415.001')
dt26_tool09=Tool(name=u'Лабopaтopнaя посуда', parameters=u'клacc точности не ниже 2', standarts=u'')
dt26_tool10=Tool(name=u'Прибор для контроля параметров микроклимата Testo 622', parameters=u'абсолютные погрешности измерений: температура,°С: ±0,4+1 мл.разр.; влажность (при 25 °С),%: ±2+1 мл.разр.; абсолютное давление,гПа: ±3+1 мл.разр.', standarts=u'')
dt26_tool11=Tool(name=u'Вода дистиллированная', parameters=u'', standarts=u'ГOCT 6709-72')
dt27_tool01=Tool(name=u'Cчeтчик аэрозольных частиц Solair 3100+', parameters=u'пределы допускаемой относительной погрешности ±8,0%', standarts=u'(зaв. № 100804002)')
dt27_tool02=Tool(name=u'Разбавитель аэрозоля DIL 554', parameters=u'', standarts=u'')
dt27_tool03=Tool(name=u'Генератор аэрозоля ATM 226', parameters=u'', standarts=u'')
dt27_tool04=Tool(name=u'Осушитель воздуха DDU 570/H', parameters=u'', standarts=u'')
dt27_tool05=Tool(name=u'Kaмepa смесительная аэрозольная КСА-1', parameters=u'', standarts=u'ШДЕК.418313.001')
dt27_tool06=Tool(name=u'Стандартные образцы гранулометрического состава на основе монодисперсных полистирольных латексов: ОГС-02ЛМ, ОГС-04ЛМ, ОГС-09ЛМ', parameters=u'границы относительной погрешности аттестованного значения (Р=0,95) ±5%', standarts=u'')
dt27_tool07=Tool(name=u'Pacxoдомep-счeтчик газа РГС-1', parameters=u'пределы допускаемой относительной погрешности ±1,0%', standarts=u'')
dt27_tool08=Tool(name=u'Упpaвляющий вычислительный комплекс УВК-01', parameters=u'', standarts=u'ШДЕК.421415.001')
dt27_tool09=Tool(name=u'Лабораторная посуда', parameters=u'Knacc точности не ниже 2', standarts=u'')
dt27_tool10=Tool(name=u'Прибор для контроля параметров микроклимата Testo 622',
                 parameters=u'абсолютные погрешности измерений: температура,°С: ±0,4+1 мл.разр.; влажность (при 25 °С),%: ±2+1 мл.разр.; абсолютное давление,гПа: ±3+1мл.разр.',
                 standarts=u'')
dt27_tool11=Tool(name=u'Вода дистиллированная', parameters=u'', standarts=u'ГOCT 6709-72')
# Назначение поверочного оборудования для типа оборудования devtype1 (СНС-ИФГ)
# devtype1.required_tools.append(dt1_tool01)
# devtype1.required_tools.append(dt1_tool02)
# devtype1.required_tools.append(dt1_tool03)
# devtype1.required_tools.append(dt1_tool04)

# Назначение поверочного оборудования для типа оборудования devtype2 (ВАД-40М)
devtype2.required_tools.append(dt2_tool01)
devtype2.required_tools.append(dt2_tool02)
devtype2.required_tools.append(dt2_tool03)
devtype2.required_tools.append(dt2_tool04)
devtype2.required_tools.append(dt2_tool05)
devtype2.required_tools.append(dt2_tool06)
devtype2.required_tools.append(dt2_tool07)
devtype2.required_tools.append(dt2_tool08)
# Назначение поверочного оборудования для типа оборудования devtype3 (ДМК-21)
devtype3.required_tools.append(dt3_tool01)
devtype3.required_tools.append(dt3_tool02)
devtype3.required_tools.append(dt3_tool03)
devtype3.required_tools.append(dt3_tool04)
devtype3.required_tools.append(dt3_tool05)
devtype3.required_tools.append(dt3_tool06)
devtype3.required_tools.append(dt3_tool07)
devtype3.required_tools.append(dt3_tool08)
# Назначение поверочного оборудования для типа оборудования devtype4 (ИГ-9)
devtype4.required_tools.append(dt4_tool01)
devtype4.required_tools.append(dt4_tool02)
devtype4.required_tools.append(dt4_tool03)
devtype4.required_tools.append(dt4_tool04)
devtype4.required_tools.append(dt4_tool05)
devtype4.required_tools.append(dt4_tool06)
devtype4.required_tools.append(dt4_tool07)
devtype4.required_tools.append(dt4_tool08)
# Назначение поверочного оборудования для типа оборудования devtype5 (ИКАР-Л)
devtype5.required_tools.append(dt5_tool01)
devtype5.required_tools.append(dt5_tool02)
devtype5.required_tools.append(dt5_tool03)
devtype5.required_tools.append(dt5_tool04)
devtype5.required_tools.append(dt5_tool05)

# Назначение поверочного оборудования для типа оборудования devtype6 (ИКОНЭТ-МП)
devtype6.required_tools.append(dt6_tool01)
devtype6.required_tools.append(dt6_tool02)

# Назначение поверочного оборудования для типа оборудования devtype7 (ИФГ-М)
devtype7.required_tools.append(dt7_tool01)
devtype7.required_tools.append(dt7_tool02)
devtype7.required_tools.append(dt7_tool03)

# Назначение поверочного оборудования для типа оборудования devtype8 (ОЭАС-05)
devtype8.required_tools.append(dt8_tool01)
devtype8.required_tools.append(dt8_tool02)
devtype8.required_tools.append(dt8_tool03)
devtype8.required_tools.append(dt8_tool04)
devtype8.required_tools.append(dt8_tool05)

# Назначение поверочного оборудования для типа оборудования devtype9 (ПГА-6)
devtype9.required_tools.append(dt9_tool01)
devtype9.required_tools.append(dt9_tool02)
devtype9.required_tools.append(dt9_tool03)
devtype9.required_tools.append(dt9_tool04)
devtype9.required_tools.append(dt9_tool05)
devtype9.required_tools.append(dt9_tool06)
devtype9.required_tools.append(dt9_tool07)
devtype9.required_tools.append(dt9_tool08)
devtype9.required_tools.append(dt9_tool09)

# Назначение поверочного оборудования для типа оборудования devtype10 (РОДНИК-6)
devtype10.required_tools.append(dt10_tool01)
devtype10.required_tools.append(dt10_tool02)
devtype10.required_tools.append(dt10_tool03)
devtype10.required_tools.append(dt10_tool04)
devtype10.required_tools.append(dt10_tool05)
devtype10.required_tools.append(dt10_tool06)
devtype10.required_tools.append(dt10_tool07)

# Назначение поверочного оборудования для типа оборудования devtype11 (РОСА-10)
devtype11.required_tools.append(dt11_tool01)
devtype11.required_tools.append(dt11_tool02)
devtype11.required_tools.append(dt11_tool03)
devtype11.required_tools.append(dt11_tool04)
devtype11.required_tools.append(dt11_tool05)
devtype11.required_tools.append(dt11_tool06)
devtype11.required_tools.append(dt11_tool07)
devtype11.required_tools.append(dt11_tool08)
devtype11.required_tools.append(dt11_tool09)
devtype11.required_tools.append(dt11_tool10)
devtype11.required_tools.append(dt11_tool11)

# Назначение поверочного оборудования для типа оборудования devtype12 (СФГ-М)
devtype12.required_tools.append(dt12_tool01)
devtype12.required_tools.append(dt12_tool02)
devtype12.required_tools.append(dt12_tool03)
devtype12.required_tools.append(dt12_tool04)
devtype12.required_tools.append(dt12_tool05)
devtype12.required_tools.append(dt12_tool06)
devtype12.required_tools.append(dt12_tool07)
devtype12.required_tools.append(dt12_tool08)
devtype12.required_tools.append(dt12_tool09)
devtype12.required_tools.append(dt12_tool10)
devtype12.required_tools.append(dt12_tool11)

# Назначение поверочного оборудования для типа оборудования devtype13 (Счетчик)
devtype13.required_tools.append(dt13_tool01)
devtype13.required_tools.append(dt13_tool02)
devtype13.required_tools.append(dt13_tool03)
devtype13.required_tools.append(dt13_tool04)
devtype13.required_tools.append(dt13_tool05)
devtype13.required_tools.append(dt13_tool06)
devtype13.required_tools.append(dt13_tool07)
devtype13.required_tools.append(dt13_tool08)
devtype13.required_tools.append(dt13_tool09)
devtype13.required_tools.append(dt13_tool10)
devtype13.required_tools.append(dt13_tool11)

# Назначение поверочного оборудования для типа оборудования devtype14 (ФП 12)
devtype14.required_tools.append(dt14_tool01)
devtype14.required_tools.append(dt14_tool02)
devtype14.required_tools.append(dt14_tool03)
devtype14.required_tools.append(dt14_tool04)
devtype14.required_tools.append(dt14_tool05)

# Назначение поверочного оборудования для типа оборудования devtype15 (ФЛЮОРИТ-Ц)
devtype15.required_tools.append(dt15_tool01)
devtype15.required_tools.append(dt15_tool02)
devtype15.required_tools.append(dt15_tool03)
devtype15.required_tools.append(dt15_tool04)
devtype15.required_tools.append(dt15_tool05)
devtype15.required_tools.append(dt15_tool06)
devtype15.required_tools.append(dt15_tool07)
devtype15.required_tools.append(dt15_tool08)
devtype15.required_tools.append(dt15_tool09)

# Назначение поверочного оборудования для типа оборудования devtype16 (ЭССА)
devtype16.required_tools.append(dt16_tool01)
devtype16.required_tools.append(dt16_tool02)
devtype16.required_tools.append(dt16_tool03)
devtype16.required_tools.append(dt16_tool04)
devtype16.required_tools.append(dt16_tool05)
devtype16.required_tools.append(dt16_tool06)
devtype16.required_tools.append(dt16_tool07)
devtype16.required_tools.append(dt16_tool08)
devtype16.required_tools.append(dt16_tool09)
devtype16.required_tools.append(dt16_tool10)
devtype16.required_tools.append(dt16_tool11)

# Назначение поверочного оборудования для типа оборудования devtype17 (МИ2705-2001)
devtype17.required_tools.append(dt17_tool01)
devtype17.required_tools.append(dt17_tool02)
devtype17.required_tools.append(dt17_tool03)
devtype17.required_tools.append(dt17_tool04)
devtype17.required_tools.append(dt17_tool05)

# Назначение поверочного оборудования для типа оборудования devtype18 (Яуза-М.01)
devtype18.required_tools.append(dt18_tool01)
devtype18.required_tools.append(dt18_tool02)
devtype18.required_tools.append(dt18_tool03)
devtype18.required_tools.append(dt18_tool04)
devtype18.required_tools.append(dt18_tool05)
devtype18.required_tools.append(dt18_tool06)
devtype18.required_tools.append(dt18_tool07)

# Назначение поверочного оборудования для типа оборудования devtype19 (Баргузин)
devtype19.required_tools.append(dt19_tool01)
devtype19.required_tools.append(dt19_tool02)
devtype19.required_tools.append(dt19_tool03)
devtype19.required_tools.append(dt19_tool04)
devtype19.required_tools.append(dt19_tool05)
devtype19.required_tools.append(dt19_tool06)
devtype19.required_tools.append(dt19_tool07)
devtype19.required_tools.append(dt19_tool08)
devtype19.required_tools.append(dt19_tool09)
devtype19.required_tools.append(dt19_tool10)
devtype19.required_tools.append(dt19_tool11)
devtype19.required_tools.append(dt19_tool12)
devtype19.required_tools.append(dt19_tool13)
devtype19.required_tools.append(dt19_tool14)
devtype19.required_tools.append(dt19_tool15)
devtype19.required_tools.append(dt19_tool16)

# Назначение поверочного оборудования для типа оборудования devtype20 (ФП 11.2к)
devtype20.required_tools.append(dt20_tool01)
devtype20.required_tools.append(dt20_tool02)
devtype20.required_tools.append(dt20_tool03)
devtype20.required_tools.append(dt20_tool04)
devtype20.required_tools.append(dt20_tool05)
devtype20.required_tools.append(dt20_tool06)
devtype20.required_tools.append(dt20_tool07)
devtype20.required_tools.append(dt20_tool08)
devtype20.required_tools.append(dt20_tool09)

# Назначение поверочного оборудования для типа оборудования devtype21 (МИ 138-77)
devtype21.required_tools.append(dt21_tool01)
devtype21.required_tools.append(dt21_tool02)
devtype21.required_tools.append(dt21_tool03)
devtype21.required_tools.append(dt21_tool04)
devtype21.required_tools.append(dt21_tool05)
devtype21.required_tools.append(dt21_tool06)
devtype21.required_tools.append(dt21_tool07)
devtype21.required_tools.append(dt21_tool08)
devtype21.required_tools.append(dt21_tool09)
devtype21.required_tools.append(dt21_tool10)
devtype21.required_tools.append(dt21_tool11)
devtype21.required_tools.append(dt21_tool12)
devtype21.required_tools.append(dt21_tool13)
devtype21.required_tools.append(dt21_tool14)
devtype21.required_tools.append(dt21_tool15)
devtype21.required_tools.append(dt21_tool16)
devtype21.required_tools.append(dt21_tool17)
devtype21.required_tools.append(dt21_tool18)
devtype21.required_tools.append(dt21_tool19)
devtype21.required_tools.append(dt21_tool20)
devtype21.required_tools.append(dt21_tool21)
devtype21.required_tools.append(dt21_tool22)
devtype21.required_tools.append(dt21_tool23)
devtype21.required_tools.append(dt21_tool24)
devtype21.required_tools.append(dt21_tool25)
devtype21.required_tools.append(dt21_tool26)
devtype21.required_tools.append(dt21_tool27)
devtype21.required_tools.append(dt21_tool28)
devtype21.required_tools.append(dt21_tool29)
devtype21.required_tools.append(dt21_tool30)
devtype21.required_tools.append(dt21_tool31)
devtype21.required_tools.append(dt21_tool32)
devtype21.required_tools.append(dt21_tool33)
devtype21.required_tools.append(dt21_tool34)
devtype21.required_tools.append(dt21_tool35)
devtype21.required_tools.append(dt21_tool36)
devtype21.required_tools.append(dt21_tool37)

# Назначение поверочного оборудования для типа оборудования devtype22 (РОДНИК-4)
devtype22.required_tools.append(dt22_tool01)
devtype22.required_tools.append(dt22_tool02)

# Назначение поверочного оборудования для типа оборудования devtype23 (Solair 5100)
devtype23.required_tools.append(dt23_tool01)
devtype23.required_tools.append(dt23_tool02)
devtype23.required_tools.append(dt23_tool03)
devtype23.required_tools.append(dt23_tool04)
devtype23.required_tools.append(dt23_tool05)
devtype23.required_tools.append(dt23_tool06)
devtype23.required_tools.append(dt23_tool07)
devtype23.required_tools.append(dt23_tool08)
devtype23.required_tools.append(dt23_tool09)
devtype23.required_tools.append(dt23_tool10)

#Назначение поверочного оборудования для типа оборудования devtype24 (ПК ГТА-0.3-002)
devtype24.required_tools.append(dt24_tool01)
devtype24.required_tools.append(dt24_tool02)
devtype24.required_tools.append(dt24_tool03)
devtype24.required_tools.append(dt24_tool04)
devtype24.required_tools.append(dt24_tool05)
devtype24.required_tools.append(dt24_tool06)
devtype24.required_tools.append(dt24_tool07)
devtype24.required_tools.append(dt24_tool08)
devtype24.required_tools.append(dt24_tool09)
devtype24.required_tools.append(dt24_tool10)
devtype24.required_tools.append(dt24_tool11)
devtype24.required_tools.append(dt24_tool12)

#Назначение поверочного оборудования dля типа оборудования devtype25 (Remote 5010)
devtype25.required_tools.append(dt25_tool01)
devtype25.required_tools.append(dt25_tool02)
devtype25.required_tools.append(dt25_tool03)
devtype25.required_tools.append(dt25_tool04)
devtype25.required_tools.append(dt25_tool05)
devtype25.required_tools.append(dt25_tool06)
devtype25.required_tools.append(dt25_tool07)
devtype25.required_tools.append(dt25_tool08)
devtype25.required_tools.append(dt25_tool09)
devtype25.required_tools.append(dt25_tool10)
devtype25.required_tools.append(dt25_tool11)

#Назначение поверочного оборудования для типа оборудования devtype26 (ПKЗB-906)
devtype26.required_tools.append(dt26_tool01)
devtype26.required_tools.append(dt26_tool02)
devtype26.required_tools.append(dt26_tool03)
devtype26.required_tools.append(dt26_tool04)
devtype26.required_tools.append(dt26_tool05)
devtype26.required_tools.append(dt26_tool06)
devtype26.required_tools.append(dt26_tool07)
devtype26.required_tools.append(dt26_tool08)
devtype26.required_tools.append(dt26_tool09)
devtype26.required_tools.append(dt26_tool10)
devtype26.required_tools.append(dt26_tool11)

#Назначение поверочного оборудования для типа оборудования devtype27 (ОЭАС-05)
devtype27.required_tools.append(dt27_tool01)
devtype27.required_tools.append(dt27_tool02)
devtype27.required_tools.append(dt27_tool03)
devtype27.required_tools.append(dt27_tool04)
devtype27.required_tools.append(dt27_tool05)
devtype27.required_tools.append(dt27_tool06)
devtype27.required_tools.append(dt27_tool07)
devtype27.required_tools.append(dt27_tool08)
devtype27.required_tools.append(dt27_tool09)
devtype27.required_tools.append(dt27_tool10)
devtype27.required_tools.append(dt27_tool11)

#Группы запросов
## Группы запросов для типа оборудования devtype1 (СНС-ИФГ)
#dt1_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
#dt1_gr0.device_type.append(devtype1)
#dt1_gr1=QuestionGroup(caption=u'Подготовка к поверке', num=1, report _caption=False)
#dt1_gr1.device_type.append(devtype1)
#dt1_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2. report_caption=True)
#dt1_gr2. device_type.append(devtype1)
#dt1_gr3=QuestionGroup(caption=u'Определение относительной погрешности воспроизведения коэффициентов пропускания',
#num=3,
#report_caption=True)
#dt1_gr3.devicetype.append(devtype1)
#dt1_gr4=QuestionGroup(caption=u'Определение относительной погрешности воспроизведения относительных различий'
#u'коэффициентов пропускания', num=4, report_caption=True)
#dt1_gr4.device_type.append(devtype1)

## Группы запросов для типа оборудования devtype2 (ВАД-40М)
dt2_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt2_gr0.device_type.append(devtype2)
dt2_gr1 =QuestionGroup(caption=u'Подготовка к поверке', num=1, report_caption=False)
dt2_gr1.device_type.append(devtype2)
dt2_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt2_gr2.device_type.append(devtype2)
dt2_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt2_gr3.device_type.append(devtype2)
dt2_gr4=QuestionGroup(caption=u'Определение приведенной погрешности', num=4, report_caption=True)
dt2_gr4.device_type.append(devtype2)

## Группы запросов для типа оборудования devtype3 (ДМК-21)
dt3_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt3_gr0.device_type.append(devtype3)
dt3_gr1 =QuestionGroup(caption=u'Внешний осмотр', num=1, repon_caption=True)
dt3_gr1.device_type.append(devtype3)
dt3_gr2=QuestionGroup(caption=u'Определение погрешности измерения эквивалентных значений концентраций, воспроизводимых'
                              u' поверочным приспособлением - набором отражающих поверхностей специализированным (НОПС)',
                      num=2, report_caption=True)
dt3_gr2.device_type.append(devtype3)
dt3_gr3=QuestionGroup(caption=u'Определение погрешности расхода газовой смеси',
                      num=3, report_caption=True)
dt3_gr3.device_type.append(devtype3)

## Группы запросов для типа оборудования devtype4 (ИГ-9)
dt4_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt4_gr0.device_type.append(devtype4)
dt4_gr1 =QuestionGroup(caption=u'Подготовка к поверке', num=1, report_caption=False)
dt4_gr1.device_type.append(devtype4)
dt4_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt4_gr2.device_type.append(devtype4)
dt4_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt4_gr3.device_type.append(devtype4)
dt4_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4, report_caption=True)
dt4_gr4.device_type.append(devtype4)

## Группы запросов для типа оборудования devtype5 (ИКАР-Л)
dt5_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt5_gr0.device_type.append(devtype5)
dt5_gr1=QuestionGroup(caption=u'Подготовка к поверке', num=1, report_caption=False)
dt5_gr1.device_type.append(devtype5)
dt5_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt5_gr2.device_type.append(devtype5)
dt5_gr3=QuestionGroup(caption=u'Опробование (калибровка)', num=3, report_caption=False)
dt5_gr3.device_type.append(devtype5)
dt5_gr4=QuestionGroup(caption=u'Определение основной абсолютной погрешности', num=4, report_caption=True)
dt5_gr4.device_type.append(devtype5)

## Группы запросов для типа оборудования devtype6 (ИКОНЭТ-МП)
dt6_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt6_gr0.device_type.append(devtype6)
dt6_gr1=QuestionGroup(caption=u'Подготовка к поверке', num=1, report_caption=False)
dt6_gr1.device_type.append(devtype6)
dt6_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt6_gr2.device_type.append(devtype6)
dt6_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=False)
dt6_gr3.device_type.append(devtype6)
dt6_gr4=QuestionGroup(caption=u'Аттестация кювет', num=4, report_caption=True)
dt6_gr4.device_type.append(devtype6)
dt6_gr5=QuestionGroup(caption=u'Определение предела допускаемой погрешности', num=5, report_caption=True)
dt6_gr5 .device_type.append(devtype6)

## Группы запросов для типа оборудования devtype7 (ИФГ-М)
dt7_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt7_gr0.device_type.append(devtype7)
dt7_gr1 =QuestionGroup(caption=u'Внешний осмотр', num=1, report_caption=True)
dt7_gr1.device_type.append(devtype7)
dt7_gr2=QuestionGroup(caption=u'Опробование', num=2, report_caption=True)
dt7_gr2.device_type.append(devtype7)
dt7_gr3=QuestionGroup(caption=u'Определение основной погрешности', num=3, report_caption=True)
dt7_gr3.device_type.append(devtype7)

## Группы запросов для типа оборудования devtype8 (ОЭАС-05)
dt8_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt8_gr0.device_type.append(devtype8)
dt8_gr1=QuestionGroup(caption=u'Внешний осмотр и опробование', num=1, report_caption=True)
dt8_gr1.device_type.append(devtype8)
dt8_gr2=QuestionGroup(caption=u'Проверка объемного расхода аэрозольной пробы', num=2, report_caption=True)
dt8_gr2.device_type.append(devtype8)
dt8_gr3=QuestionGroup(caption=u'Определение относительной погрешности измерений объема аэрозольной пробы', num=3,
                      report_caption=True)
dt8_gr3.device_type.append(devtype8)
dt8_gr4=QuestionGroup(caption=u'Проверка эффективности счета частиц аэрозоля монодисперсных латексов диаметрами 0.5 и '
                              u'5.0 мкм', num=4, report_caption=True)
dt8_gr4.device_type.append(devtype8)
dt8_gr5=QuestionGroup(caption=u'Определение основной относительной погрешности измерений счетной концентрации частиц',
                      num=5, report_caption=True)
dt8_gr5.device_type.append(devtype8)

## Группы запросов для типа оборудования devtype9 (ПГА-6)
dt9_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt9_gr0.device_type.append(devtype9)
dt9_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt9_gr1.device_type.append(devtype9)
dt9_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt9_gr2.device_type.append(devtype9)
dt9_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt9_gr3.device_type.append(devtype9)
dt9_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4,
                      report_caption=True)
dt9_gr4.device_type.append(devtype9)

## Группы запросов для типа оборудования devtype10 (РОДНИК-6)
dt10_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt10_gr0.device_type.append(devtype10)
dt10_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt10_gr1.device_type.append(devtype10)
dt10_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt10_gr2.device_type.append(devtype10)
dt10_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt10_gr3.device_type.append(devtype10)
dt10_gr4=QuestionGroup(caption=u'Опробование метрологических характеристик', num=4,
                       report_caption=True)
dt10_gr4.device_type.append(devtype10)

## Группы запросов для типа оборудования devlype11 (РОСА-10)
dt11_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt11_gr0.device_type.append(devtype11)
dt11_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt11_gr1.device_type.append(devtype11)
dt11_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt11_gr2.device_type.append(devtype11)
dt11_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt11_gr3.device_type.append(devtype11)
dt11_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4,
                       report_caption=True)
dt11_gr4.device_type.append(devtype11)

## Группы запросов для типа оборудования devtype12 (СФГ-М)
dt12_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt12_gr0.device_type.append(devtype12)
dt12_gr1=QuestionGroup(caption=u'Внешний осмотр', num=1, report_caption=True)
dt12_gr1.device_type.append(devtype12)
dt12_gr2=QuestionGroup(caption=u'Опробование', num=2, report_caption=True)
dt12_gr2.device_type.append(devtype12)
dt12_gr3=QuestionGroup(caption=u'Определение метрологических характеристик', num=3,
                       report_caption=True)
dt12_gr3.device_type.append(devtype12)

## Группы запросов для типа оборудования devtype13 (Счетчик)
dt13_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt13_gr0.device_type.append(devtype13)
dt13_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt13_gr1.device_type.append(devtype13)
dt13_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt13_gr2.device_type.append(devtype13)
dt13_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt13_gr3.device_type.append(devtype13)
dt13_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4,
                       report_caption=True)
dt13_gr4.device_type.append(devtype13)

## Группы запросов для типа оборудования devtype14 (ФП 12)
dt14_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt14_gr0.device_type.append(devtype14)
dt14_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num= 1, report_caption=False)
dt14_gr1.device_type.append(devtype14)
dt14_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt14_gr2.device_type.append(devtype14)
dt14_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt14_gr3.device_type.append(devtype14)
dt14_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4,
                       report_caption=True)
dt14_gr4.device_type.append(devtype14)

## Группы запросов для типа оборудования devtype15 (ФЛЮОРИТ-Ц)
dt15_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt15_gr0.device_type.append(devtype15)
dt15_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt15_gr1.device_type.append(devtype15)
dt15_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt15_gr2.device_type.append(devtype15)
dt15_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt15_gr3.device_type.append(devtype15)
dt15_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4,
                       report_caption=True)
dt15_gr4.device_type.append(devtype15)

## Группы запросов для типа оборудования devtype16 (ЭССА)
dt16_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt16_gr0.device_type.append(devtype16)
dt16_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt16_gr1.device_type.append(devtype16)
dt16_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt16_gr2.device_type.append(devtype16)
dt16_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt16_gr3.device_type.append(devtype16)
dt16_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4,
                       report_caption=True)
dt16_gr4.device_type.append(devtype16)

## Группы запросов для типа оборудования devtype17 (МИ2705-2001)
dt17_gr1=QuestionGroup(caption=u'Внешний осмотр', num=1, report_caption=True)
dt17_gr1.device_type.append(devtype17)
dt17_gr2=QuestionGroup(caption=u'Опробование', num=2, report_caption=True)
dt17_gr2.device_type.append(devtype17)
dt17_gr3=QuestionGroup(caption=u'Определение метрологических характеристик', num=3,
                       report_caption=True)
dt17_gr3.device_type.append(devtype17)

## Группы запросов для типа оборудования devtype18 (Яуза-М.01)
dt18_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt18_gr0.device_type.append(devtype18)
dt18_gr1=QuestionGroup(caption=u'Внешний осмотр', num=1, report_caption=True)
dt18_gr1.device_type.append(devtype18)
dt18_gr2=QuestionGroup(caption=u'Опробование', num=2, report_caption=True)
dt18_gr2.device_type.append(devtype18)
dt18_gr3=QuestionGroup(caption=u'Определение основной погрешности (ПГС)', num=3, report_caption=True)
dt18_gr3.device_type.append(devtype18)
dt18_gr4=QuestionGroup(caption=u'Определение основной погрешности (CHC-ИФГ)', num=4, report_caption=True)
dt18_gr4.device_type.append(devtype18)

## Группы запросов для типа оборудования devtype19 (Баргузин)
dt19_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt19_gr0.device_type.append(devtype19)
dt19_gr1=QuestionGroup(caption=u'Внешний осмотр', num=1, report_caption=True)
dt19_gr1.device_type.append(devtype19)
dt19_gr2=QuestionGroup(caption=u'Опробование', num=2, report_caption=True)
dt19_gr2.device_type.append(devtype19)
dt19_gr3=QuestionGroup(caption=u'Определение метрологических характеристик', num=3, report_caption=True)
dt19_gr3.device_type.append(devtype19)

## Группы запросов для типа оборудования devtype20 (ФП11.2к)
dt20_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt20_gr0.device_type.append(devtype20)
dt20_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt20_gr1.device_type.append(devtype20)
dt20_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt20_gr2.device_type.append(devtype20)
dt20_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt20_gr3.device_type.append(devtype20)
dt20_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4, report_caption=True)
dt20_gr4.device_type.append(devtype20)

## Группы запросов для типа оборудования devtype21 (МИ 138-77)
dt21_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt21_gr0.device_type.append(devtype21)
dt21_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt21_gr1.device_type.append(devtype21)
dt21_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt21_gr2.device_type.append(devtype21)
dt21_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt21_gr3.device_type.append(devtype21)
dt21_gr4=QuestionGroup(caption=u'Определение погрешности спиртомера', num=4, report_caption=True)
dt21_gr4.device_type.append(devtype21)

## Группы запросов для типа оборудования devtype22 (РОДНИК-4)
dt22_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt22_gr0.device_type.append(devtype22)
dt22_gr1=QuestionGroup(caption=u'Внешний осмотр', num=1, report_caption=True)
dt22_gr1.device_type.append(devtype22)
dt22_gr2=QuestionGroup(caption=u'Опробование', num=2, report_caption=True)
dt22_gr2.device_type.append(devtype22)
dt22_gr3=QuestionGroup(caption=u'Определение метрологических характеристик', num=3, report_caption=True)
dt22_gr3.device_type.append(devtype22)

## Группы запросов для типа оборудования devtype23 (Solair 5100)
dt23_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt23_gr0.device_type.append(devtype23)
dt23_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt23_gr1.device_type.append(devtype23)
dt23_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt23_gr2.device_type.append(devtype23)
dt23_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt23_gr3 .device_type.append(devtype23)
dt23_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4, report_caption=True)
dt23_gr4.device_type.append(devtype23)

## Группы запросов для типа оборудования devtype24 (ПК ГТА-0.3-002)
dt24_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt24_gr0.device_type.append(devtype24)
dt24_gr1 =QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt24_gr1.device_type.append(devtype24)
dt24_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt24_gr2.device_type.append(devtype24)
dt24_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt24_gr3.device_type.append(devtype24)
dt24_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4, report_caption=True)
dt24_gr4.device_type.append(devtype24)

## Группы запросов для типа оборудования devtype25 (Remote 5010)
dt25_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt25_gr0.device_type.append(devtype25)
dt25_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt25_gr1.device_type.append(devtype25)
dt25_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt25_gr2.device_type.append(devtype25)
dt25_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt25_gr3.device_type.append(devtype25)
dt25_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4, report_caption=True)
dt25_gr4.device_type.append(devtype25)

## Группы запросов для типа оборудования devtype26 (ПКЗВ-906)
dt26_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt26_gr0.device_type.append(devtype26)
dt26_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt26_gr1.device_type.append(devtype26)
dt26_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt26_gr2.device_type.append(devtype26)
dt26_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt26_gr3.device_type.append(devtype26)
dt26_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4, report_caption=True)
dt26_gr4.device_type.append(devtype26)

## Группы запросов для типа оборудования devtype27 (ОЭАС-05)
dt27_gr0=QuestionGroup(caption=u'Общие условия поверки', num=0, report_caption=False)
dt27_gr0.device_type.append(devtype27)
dt27_gr1=QuestionGroup(caption=u'Подготовка к проведению поверки', num=1, report_caption=False)
dt27_gr1.device_type.append(devtype27)
dt27_gr2=QuestionGroup(caption=u'Внешний осмотр', num=2, report_caption=True)
dt27_gr2.device_type.append(devtype27)
dt27_gr3=QuestionGroup(caption=u'Опробование', num=3, report_caption=True)
dt27_gr3.device_type.append(devtype27)
dt27_gr4=QuestionGroup(caption=u'Определение метрологических характеристик', num=4, report_caption=True)
dt27_gr4.device_type.append(devtype27)

# Типы запросов
qtype_value = QuestionType(typename = u'VALUE', description=u'Ввод значения')
qtype_choose = QuestionType(typename = u'CHOOSE', description=u'Выбор значения')
qtype_confirm = QuestionType(typename = u'CONFIRM', description=u'Пoдтвepждeниe исполнения')

# Запросы
## Запросы для групп запросов для типа оборудования devtype1 (СНС-ИФГ)
#temperature = Parameter(variable_name = u't', description = u'Температура', readable_name = u't', unit = celsius)
#pressure = Parameter(variable_name = u'p', description = u'Давление', readable name = u'p', unit = kilopascal)
#humidity = Parameter(variable_name = u'h', description = u'Отн. влажность', readable_name = u'h', unit = rel_percent)
#Question(question_group=dt1_gr0, num=1, caption=u'Измерение параметров окружающей среды',
#text=u'Укажите текущие параметры окружающей среды.',
#condition=u'(15 <= t <= 25) and (90.6 <=р <= 104.8) and (30 <= h <= 80)',
#measurable_parameters=[temperature, pressure, humidity],
#params=u't $ p $ h',
#param_comments=u'Температура, °C $ Давление, кПа $ Отн. влажность воздуха, %',
#param_names=u't $ p $ h',param_hints=u'20 $ 100 $ 70', calculations=u'', iterations=0,
#reportstring=u'<br>Температура окружающей среды: {t} °C<br>Давление: {p} кПа'
#u'<br>Относительная влажность воздуха: {h}%',
#conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений'
#u'(Темепература: 15 ≤t ≤25 °С; Давление: 90.6 ≤р ≤ 104.8 кПа; Влажность: 30% ≤h≤ 80%)</i>',
#conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений'
#u'(Температура: 15 ≤t ≤25 °С; Давление: 90.6 ≤р≤ 104.8 кПа; Влажность: 30% ≤h≤ 80%)</i>'
#u'<br><br>Заключение:<u> Поверка невозможна </и>',
#question_type =qtype_value)
#Question(question_group=dt1_gr1, num=1, caption=u'Установка комплекта CHC-ИФГ в спектрофотометр СФ-18',
#text=u'<р>Установите комплект СНС-ИФГ в спектрофотометр СФ-18 с помощью приставки типа УТАМ5.122.002, фиксация '
#u'положения которой должна быть проведена в кюветном отделении спектрофотометра в следующей '
#u'последовательности:'
#u'<р>1) включите спектрофотометр в соответствии с его ЭД, установите указатель его диафрагмы на отметку 15 '
#u'мм, задействуйте кулачок Т (0-100 %), выставите показание 100% и тумблером ОТРАБОТКА-ВЫКЛ. отключите '
#u'двигатель отработки;'
#u'<р>2) откройте крышку кюветного отделения, установите максимальное отверстие диафрагмы приставки и '
#u'введите приставку, свободную от комплекта СНС-ИФГ, в зазор между призмами и плитой - основанием кюветного '
#u'отделения так, чтобы фиксатор комплекта СНС-ИФГ и диафрагма приставки легли соответственно на правое и'
#u'левое входные отверстия в фотометрический шар;'
#u'<р>3) включите тумблер ОТРАБОТКА и отыщите положение приставки на плите-основании кюветного отделения при '
#u'котором показания отсчетногоустройства спектрофотометра окажутся максимальными;'
#u'<р>4) выполните фиксацию пластины и плиты-основания кюветного отделения спектрофотометра в найденном'
#u'положении приставки так, чтобы при ее извлечении из кюветного отделения и повторной установке, приставка'
#u'занимала бы прежнее положение.',
#condition=u'x and у and z and k', params=u'x $y$z$k', calculation=u'',
#param_comments=u'Пункт 1 выполнен $ Пункт 2 выполнен $ Пункт 3 выполнен $ Пункт 4 выполнен', iterations=0,
#question_type=qtype_confirm)
#Question(question_group=dt1_gr2, num=1, caption=u'Установление соответствия требованиям к внешнему виду',
#text=u'<р>При внешнем осмотре должно быть установлено соответствие следующим требованиям:'
#u'<р>1) соответствие маркировки и комплектности комплекта СНС-ИФГ требованиям НТД;'
#u'<р>2) отсутствие механических повреждений и загрязнений, влияющих на работоспособность комплекта СНС-ИФГ.',
#condition=u'x and у', params=u'x $ у', param_comments=u'Требование №1 выполнено $ Требование №2 выполнено',
#calculation=u'', iterations=0, question_type=qtype_confirm,
#conclusion_success=u'<br>Внешний вид соответствует требованиям',
#conclusion_failure=u'<br>Внешний вид не соответствует требованиям'
#u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>)
#Question(question_group=dt1_gr3, num=1, caption=u'Подготовка к определению относительной погрешности воспроизведения'
#u'коэффициентов пропускания',
#text=u'<p>Выполните следующие действия:'
#u'<р>1) в щель фиксатора комплекта СНС-ИФГ приставки, установленной в кюветное отделение спектрофотометра '
#u'СФ-18, введите комплект СНС-ИФГ до первого щелчка фиксатора, установив, тем самым, в окошке фиксатора'
#u'окошко № 1 комплекта СНС-ИФГ, не содержащее светофильтра..'
#u'<р>2) включите спектрофотометр, настроив его на измерение коэффициентов пропускания в диапазоне 0 - 100%, '
#u'при длине волны 464 нм. Установите отсчетное устройство на линию бланка 100%, путем измерения отверстия '
#u'диафрагмы приставки.'
#u'<р>3) вдвиньте комплект СНС-ИФГ на один шаг в фиксатор (до щелчка}, установите тем самым в окошке '
#u'фиксатора светофильтр, расположенный в окошке № 2 комплекта СНС-ИФГ.',
#condition=u'x and у and z', params=u'x $ у $ z', calculation=u'',
#param_comments=u'Действие №1 выполнено $ Действие №2 выполнено $ Действие №3 выполнено', iterations=0,
#question_type =qtype_confirm)
#Question(question_group=dt1_gr3, num=2, caption=u'Определение относительной погрешности воспроизведения коэффициентов '
#u'пропускания',
#tехt=u'Снимите показание отсчетного устройства.',
#condition =u'(25 <= d <= 35) and (abs(delta) <= 1)', params=u'd $ delta',
#param_comments=u'Коэффициент пропускания, %', calculation=u'delta=((d-K2)/K2)*100',
#param_names=u'K<sub>2</sub>', param_hints=u'K2', iterations=0, question_type =qtype_value,
#reportstring=u'<br>K<sub>2</sub>={d}% абс., δ={delta}%',
#conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений'
#u'(25 ≤ K<sub>2</sub> ≤35, δ≤ ±l%)</i>'
#conclusion_failure =u'<br><i>Значения лежат за пределами заданных ограничений ’
#u'(25 ≤K<sub>2</sub> ≤35, δ≤±1%)</i>'
#u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>)
#Question(question_group=dt1_gr4, num=1, caption=u'Подготовка к определению относительной погрешности воспроизведения'
#u'относительных различий коэффициентов пропускания',
#text=u'<p>Выполните следующие действия:'
#u'<р>1) введите комплект СНС-ИФГ в щель фиксатора приставки. Совместите окошко фиксатора с окошком № 2
#u'комплекта СНС-ИФГ;'
#u'<р>2) включите спектрофотометр, установите на нем длину волны 464нм и задействуйте кулачок Т (0 - 100%). '
#u'Регулируя размер отверстия диафрагмы приставки, установите отсчетное устройство спектрофотометра на линию '
#u'бланка 100%. В соответствии с эксплуатационной документацией спектрофотометра задействуйте кулачок Т (90'
#u'- 110%);',
#condition=u'x and у', params=u'x $ у', param_comments=u'Действие №1 выполнено $ Действие №2 выполнено',
#calculation=u'', iterations=0, question_type=qtype_confirm)
#Question(question_group=dt1_gr4, num=2, caption=u'Определение относительной погрешности воспроизведения относительных '
#u'различий коэффициентов пропускания',
#text=u'<p>Введите положение отсчетного устройства на бланке в качестве координат точки 1&INDEX'
#u'<р>Совместите окошко №3 комплекта СНС-ИФГ с окошком фиксатора и введите новое положение отсчетного '
#u'устройства на бланке в качестве координат точки 2&INDEX'
#u'<р>Совместите окошко №4 комплекта СНС-ИФГ с окошком фиксатора и введите новое положение отсчетного '
#u'устройства на бланке в качестве координат точки 3&INDEX'
#u'<р>Вновь совместите окошко №2 комплекта СНС-ИФГ с окошком фиксатора на приставке</ul>',
#condition=u'S12 =sqrt((Tx1 - Тх2) **2+(Ty1 - Ty2)**2) ; S13=sqrt((Tx1-Tx3)**2+(Ty1-Ту3)**2)',
#params=u'Tx1 $ Ty1 $ Тх2 $ Ту2 $ ТхЗ $ ТуЗ $ S12 $ S13',
#param_comments=u'Ордината точки 1&INDEX $ Абсцисса точки 1&INDEX $ Ордината точки 2&INDEX $'
#u'Абсцисса точки 2&INDEX $ Ордината точки 3&1NDEX$ Абсцисса точки 3&INDEX',
#param_names=u'X<sub>1(</sub>&INDEX<sub>)</sub> $ Y<sub>1(</sub>&INDEX<sub >)</sub> $'
#u'X<sub>2(</sub>&INDEX<sub>)</sub> $ Y<sub>2(</sub>&INDEX<sub>)</sub> $'
#u'X<sub>3(</sub>&INDEX<sub>)</sub> $ Y<sub>3(</sub>&INDEX<sub>)</sub>',
#param_hints=u'0 $ 0 $ sin(pi/6)*P23p*10 $ cos(pi/6)*P23p*10 $ sin(pi/6)*P24p*10 $ cos(pi/6)*P24p*10',
#calculation=u'',
#iteralions=10, question_type=qtype_value,
#iterparams=u'R12 $ R13 $ Sav12 $ Sav13 $ P23 $ P24 $ delta23 $ delta24',
#itercalc=u'R12=rangedev(S12); R13=rangedev(S13); Sav12=avg(S12); Sav13=avg(S13); P23=0.1*Sav12; P24=0.1*Sav13; '
#u'delta23=((P23-P23p)/P23p)*100; delta24=((P24-P24p)/P24p)*100',
#itercond=u'(abs(delta23)<=4) and (abs(delta24)<=4)',
#conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (δ ≤ ±4%)</i>'
#u'<br><br>Заключение:<u> Оборудование годно к эксплуатации </u>',
#conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (δ ≤ ±4%)</i>'
#u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
#reportstring=u'<br>П23={Р23}% абс., δ={delta23}%<br>П24={P24}% абс., δ={delta24}%)

## Запросы для групп запросов для типа оборудования devtype2 (ВАД-40М)
Question(question_group=dt2_gr0, num=1, caption=u'Измерение параметров окружающей среды',
         text=u'Укажите текущие параметры окружающей среды и переменного тока в электросети.',
         condition=u'(18 <= t <= 22) and (р <= 107) and (h <= 80) and (215 <= u <=230) and (49.5 <=f <= 50.5)',
         params=u't $ p $ h $ u $f',
         param_comments=u'Температура, °C $ Давление, кПа $ Отн. влажность воздуха, % $ Напряжение, В $ Частота, Гц',
         param_names=u't $ р $ h $ U $ v', param_hints=u'20 $ 100 $70 $ 220 $ 50', calculation=u'', iterations=0,
         reportstring=u'<br>Температура окружающей среды: {t} °C<br>Давление: {p} кПа'
                      u'<br>Относительная влажность воздуха: (h}%<br>Напряжение питания переменного тока: {u} В'
                      u'<br>Частота переменного тока: {f} Гц',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений '
                            u'(Температура: 20±2 °С; Давление: не более 107 кПа; Влажность: не более 80%;'
                            u'Напряжение: 220+10/-5 В; Частота: 50±0.5 Гц)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений'
                            u'(Температура: 20±2 °С; Давление: не более 107 кПа; Влажность: не более 80%;'
                            u'Напряжение: 220+10/-5 В; Частота: 50±0.5 Гц)</i>'
                            u'<br><br>Заключение:<u> Поверка невозможна </u>',
         question_type=qtype_value)
Question(question_group=dt2_gr1, num=1, caption=u'Проведение подготовительных действий',
         text=u'<р>Проверьте работоспособность прибора в соответствии с п. 7 паспорта.'
              u'<р>Прогрейте прибор в течение 5 минут.',
         condition=u'x and у and z', params=u'x $ у $ z', calculation=u'',
         param_comment=u'Работоспособность проверена $ Прибор работоспособен $ Прибор прогрет', iterations=0,
         question_type=qtype_confirm,
         conclusion_failure=u'<br>Прибор показал свою неработоспособность в процессе подготовки к поверке'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>')
Question(question_group=dt2_gr2, num=1, caption=u'Установление соответствия требованиям к внешнему виду',
         text=u'<р>Установите соответствие поверяемого прибора следующим требованиям:'
              u'<р>1) на приборе не должно быть повреждений и дефектов покрытий, ухудшающих его внешний вид и '
              u'препятствующих его применению для измерений;'
              u'<р>2) надписи и обозначения на приборе должны быть четкими и соответствовать технической документации'
              u'фирмы изготовителя;'
              u'<р>3) прибор должен размещаться на рабочей поверхности стола согласно паспорту.',
         condition=u'x and у and z', params=u'x $y$z', calculations=u'',
         param_comments=u'Требование №1 выполнено $ Требование №2 выполнено $ Требование №3 выполнено', iterations=0,
         question_type=qtype_confirm,
         conclusion_success=u'<br> Внешний вид соответствует требованиям',
         conclusion_failure=u'<br>Внешний вид не соответствует требованиям'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>')
Question(question_group=dt2_gr3, num=1, caption=u'Проверка исправности прибора',
         text=u'<p>Проверьте исправность прибора в соответствии с п. 7 паспорта.',
         condition=u'x and у', params=u'x $ у', param_comments=u'Исправность проверена $ Прибор исправен',
         iterations=0,
         calculation=u'', question_type=qtype_confirm,
         conclusion_success=u'<br>Прибор исправен',
         conclusion_failure=u'<br>Прибор неисправен'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>')
Question(question_group=dt2_gr4, num=1, caption=u'Определение погрешности на образце ВН-0',
         text=u'<p>Проведите измерение массовой доли содержания воды в стандартном образце ВН-0 в соответствии с разделом '
              u'8 паспорта.',
         condition=u'abs(delta0) <= 2.5', params=u'x0 $ d0 S delta0', param_names=u'M $ R', param_hints=u'0.1 $ 100',
         param_comments=u'Результат измерений, % $ Диапазон измерений, %', iterations=0,
         calculation=u'delta0=((x0-0.1)/d0)*100',
         reportstring=u'<br>Образец ВН-0. Измеренное значение: {x0}, Погрешность: {delta0}%',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (δ ≤ ±2.5%)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (δ ≤±2.5%)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
Question(question_group=dt2_gr4, num=2, caption=u'Определение погрешности на образце ВН-1',
         text=u'<p>Проведите измерение массовой доли содержания воды в стандартном образце ВН-1 в соответствии с разделом '
              u'8 паспорта.',
         condition=u'abs(delta1) <= 2.5', params=u'x1 $ d1 $ delta1', param_names=u'M $ R', param_hints=u'1 $ 100',
         param_comments=u'Результат измерений, % $ Диапазон измерений, %', iterations=0,
         calculation=u'delta1 =((x1-1)/d1) *100',
         reportstring=u'<br>Образец ВН-1. Измеренное значение: {x1}, Погрешность: {delta1}%',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (δ ≤±2.5%)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (δ ≤±2.5%)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
Question(question_group=dt2_gr4, num=3, caption=u'Определение погрешности на образце BH-3',
         text=u'<p>Проведите измерение массовой доли содержания воды в стандартном образце ВН-3 в соответствии с разделом '
              u'8 паспорта.',
         condition=u'abs(delta3) <= 2.5', params=u'x3 $ d3 $ delta3', param_names=u'M $ R', param_hints=u'3 $ 100',
         param_comments=u'Результат измерений, %$ Диапазон измерений, %', iterations=0,
         calculation=u'delta3=((x3-3)/d3)*100',
         reportstring=u'<br>Образец BH-3. Измеренное значение: {х3}, Погрешность: {delta3}%',
         conclusion_success=u'<br><i> Значения лежат в пределах заданных ограничений (δ ≤ ±2.5%)</i>',
         conclusion_fаilure=u'<br><i>Значения лежат за пределами заданных ограничений (δ ≤ ±2.5%)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
Question(question_group=dt2_gr4, num=4, caption=u'Определение погрешности на образце ВН-6',
         tехt=u'<р>Проведите измерение массовой доли содержания воды в стандартном образце ВН-6 в соответствии с разделом '
              u'8 паспорта.',
         condition=u'abs(delta6) <= 2.5', params=u'x6 $ d6 $ delta6', param_names=u'M $ R', param_hints=u'6 $ 100',
         param_comments=u'Результат измерений, % $ Диапазон измерений, %', iterations=0,
         calculation=u'delta6=((x6-6)/d6)* 100',
         reportstring=u'<br>Образец BH-6. Измеренное значение: (х6), Погрешность: {delta6}%',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (δ ≤ ±2.5%)</i>'
                            u'<br><br>Заключение:<u> Оборудование годно к эксплуатации </u>',
         conclusion_failure=u'<br><i> Значения лежат за пределами заданных ограничений (δ ≤ ±2.5%)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
## Запросы для групп запросов для типа оборудования devtype3 (ДМК-21)
Question(question_group=dt3_gr0, num=1, caption=u'Измерение параметров окружающей среды',
         text=u'Укажите текущие параметры окружающей среды.',
         condition=u'(15 <= t <= 25) and (86 <= р <= 103) and (h <= 80)', params=u't $ p $ h',
         param_comments=u'Температура, °C $ Давление, кПа $ Отн. влажность воздуха, %',
         param_names=u't $ p $ h', param_hints=u'20 $ 100 $ 70', calculation=u'', iterations=0,
         reportstring=u'<br>Температура окружающей среды: {t} °C<br>Давление: {p) кПа'
                      u'<br>Относительная влажность воздуха: {h}%',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений '
                            u'(Температура: 15 ≤ t ≤ 25 °С; Давление: 86 ≤р ≤ 103 кПа; Влажность: до 80%)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений'
                            u'(Температура: 15 ≤ t ≤ 25 °С; Давление: 86 ≤ р ≤ 103 кПа; Влажность: до 80%)</i>'
                            u'<br><br>Заключение:<u> Поверка невозможна </u>',
         question_type=qtype_value)
Question(question_group=dt3_gr1, num=1, сарtion=u'Установление соответствия требованиям к внешнему виду',
         tеxt=u'<р>Установите соответствие поверяемого прибора следующим требованиям:'
              u'<р>1) отсутствие механических повреждений на корпусе измерительного преобразователя ДМК-21. Отсутствие '
              u'грязи, ржавчины, соответствие внешнего вида сборочному чертежу;'
              u'<р>2) наличие сопроводительной документации на измерительный преобразователь ДМК-21.',
         condition=u'x and у', params=u'x $ у', calculation=u'',
         param_comments=u'Требование №1 выполнено $ Требование №2 выполнено', iterations=0,
         question_type=qtype_confirm,
         conclusion_success=u'<br>Внешний вид соответствует требованиям', \
         conclusion_failure=u'<br> Внешний вид не соответствует требованиям' \
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>')
dt3_img1 = Image(name=u'scheme', data=loadImageData('db_images/dmk21_01.jpg'))
Question(question_group=dt3_gr2, num=1, сарtion=u'Подготовка к определению погрешности измерения эквивалентных значений '
                                                u'концентраций на 1,5-2,5 ПДК',
         images=[dt3_img1],
         text=u'<center><img src="scheme "></center><p>Выполните следующие действия:'
              u'<р>1) Соберите схему поверки согласно рисунку.'
              u' Выключатели питания на ПЭВМ, пульте проверки ДМК-21, источнике питания Б5-48, установите в '
              u'положение ВЫКЛЮЧЕНО (0), предварительно установив на приборе Б5-48 напряжение (16±0,5)В.'
              u' Установите в прибор ДМК-21 один из экземпляров НОПС, типа, соответствующего испытываемому'
              u'измерительному преобразователю, с паспортным значением эквивалентной концентрации от 1,5 ПДК до 2,5 ПДК'
              u' На пульте проверки ДМК-21 переключателями АДРЕС установите адрес 0.0 (0 - cm. разряд. 0 - мл. разряд).'
              u'<р>2) Установите на ПЭВМ выключатель питания в положение ВКЛЮЧЕНО, на пульте проверки ДМК-21 - в '
              u'положение ВКЛ, на приборе Б5-48 - в положение СЕТЬ. На пульте проверки ДМК-21 должен загореться '
              u'светодиод СЕТЬ. На экране дисплея, установив курсор на ярлык "Тест ДМК21 ”, нажмите левую кнопку мыши. На'
              u'экране дисплея должно открыться окно "Программа проверки датчика ДМК-21"'
              u'<р>3) В секции ЗАПРОС К ДАТЧИКУ в выпадающем списке АДРЕС установите адрес проверяемого преобразователя, '
              u'набирая курсором мыши в выпадающем списке адрес 0.0. В секции ПАРАМЕТРЫ НАСТРОЙКИ установите тип ПЛП'
              u'(ленты), тип продукта, соответствующие проверяемому преобразователю ДМК-21, коэффициент чувствительности '
              u'равный 1, порт, для чего, устанавливая курсор мыши поочередно на кнопку выпадающих списков ЛЕНТА, '
              u'ПРОДУКТ, КОЭФФИЦИЕНТ ЧУВСТВИТЕЛЬНОСТИ, ПОРТ, курсором мыши выберите в этих списках нужный тип ПЛП, '
              u'продукта, коэффициент чувствительности, порт, нажимая левую кнопку мыши.'
              u'<р>4) В секции ЗАПРОС К ДАТЧИКУ в выпадающем списке КОМАНДА выберите команду 15 "Ввод вида '
              u'контролируемого продукта и типа ЛЧЭ (ВТЛ)". затем установите курсор мыши на кнопку ВЫПОЛНИТЬ и нажмите '
              u'левую кнопку мыши. В секции СОСТОЯНИЕ должен появиться код посылки 10\\201H. Подайте команду 16 "Ввод'
              u'коэффициента чувствительности (ВКЧ)". В секции СОСТОЯНИЕ должен появиться код посылки 0\\30аН, '
              u'преобразователь должен войти в режим "самопроверка" (пройдет протяжка ЛЧЭ и короткий продув, не более'
              u'5 с). Затем выполните команду 2 "Запрос результата самопроверки". В секции СОСТОЯНИЕ должен появиться'
              u'код ответа 1111111 11000000.',
         condition=u'x and у and z and k', params=u'x $ у $ z $ k', calculation=u'',
         param_comments=u'Действие №1 выполнено $ Действие №2 выполнено $'
                        u' Действие №3 выполнено $ Действие №4 выполнено', iterations=0,
         question_type=qtype_confirm)
Question(question_group=dt3_gr2, num=2, caption=u'Определение погрешности измерения эквивалентных значений '
                                                u'концентраций на 1,5-2,5 ПДК',
         text=u'<p>Подайте команду 9 "Включить циклические измерения на старом пятне (ЦИСП)".'
              u'<р>При переходе светодиода №2 на панели измерительного преобразователя ДМК-21 в мигающий режим, '
              u'переведите пластину НОПС с отражающими элементами на половину хода перемещения до следующего элемента на '
              u'время 1 секунду (примерно, до погасания мигающего светодиода) и быстро верните в прежнее положение.'
              u'При выполнении следующих действий секундомером измерьте время свечения светодиодов №2 и №3 и введите'
              u'результаты измерений в поля длительностей ниже:<br>'
              u'После перехода светодиода №2 в режим постоянного свечения (ПРОДУВ №1) переведите НОПС в требуемое '
              u'положение (установите напротив окна для фотометрирования соответствующий отражающий элемент), если '
              u'необходимо определить меру на первом продуве (указывается в паспорте НОПС). При определении погрешности '
              u'измерения на втором продуве (указывается в паспорте НОПС), не совершая никаких действий, дождитесь '
              u'погасания светодиода №2 и свечения светодиода №3, и теперь переведите НОПС в нужное положение.'
              u'<р>По завершении измерительного процесса (погасание всех светодиодов на панели и выключение побудителя'
              u'расхода газа), выполните команду «ЧТЕНИЕ РЕЗУЛЬТАТА», считайте с экрана полученное значение и полученный'
              u'результат введите в поле ниже. Верните пластину НОПС в исходное положение.',
         condition=u'deltaC2=((C2-C2p)/C2p) *100',
         params=u'C2 $ t1 $ t2 $ deltaC2',
         param_comments=u'Измеренная экв. концентрация$ Длительность 1-го эксп. продува$ Длительность 2-го эксп. продува',
         param_names=u'C<sub>&lNDEX</sub> $ T<sub> 1 (</sub>&INDEX<sub>)</sub> $ T<sub>2(</sub>&INDEX<sub>)</sub>',
         param_hints=u'C2p $ 90 $ 90',
         calculation=u'',
         iterations=15, question_type=qtype_value,
         iterparams=u'C2av $ t1av $ t2av $ deltaC2av',
         itercalc=u'C2av=avg(C2); t1av=avg(t1); t2av=avg(t2); deltaC2av=avg(deltaC2)',
         itercond=u'(abs(deltaC2av)<=15) and (89 <= t1av <= 91) and (89 <= t2av <= 91)',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (δ ≤ ±15%, Т=90 ± 1с)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (δ ≤ ±15%. Т=90 ± 1с)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         reportstring=u'<br> 1,5-2,5 ПДК: T<sub>1</sub>={t1av) с, T<sub>2</sub>={t2av) с, C={C2av) ПДК. δ={deltaC2av}%')
Question(question_group=dt3_gr2, num=3, сарtion=u'Подготовка к определению погрешности измерения эквивалентных значений '
                                                u'концентраций на 4-6 ПДК',
         text=u'<р> Установите в прибор ДМК-21 один из экземпляров НОПС, типа, соответствующего испытываемому '
              u'измерительному преобразователю, с паспортным значением эквивалентной концентрации от 4 ПДК до 6 ПДК.',
         condition=u'x', params=u'x', calculation=u'',
         param_comments=u'Действие выполнено ', iterations=0,
         question_type=qtype_confirm)
Question(question_group=dt3_gr2, num=4, caption=u'Определение погрешности измерения эквивалентных значений '
                                                u'концентраций на 4-6 ПДК',
         text=u'<p>Подайте команду 9 "Включить циклические измерения на старом пятне (ЦИСП)".'
              u'<р>При переходе светодиода №2 на панели измерительного преобразователя ДМК-21 в мигающий режим, '
              u'переведите пластину НОПС с отражающими элементами на половину хода перемещения до следующего элемента на'
              u'время 1 секунду (примерно, до погасания мигающего светодиода) и быстро верните в прежнее положение.'
              u'При выполнении следующих действий секундомером измерьте время свечения светодиодов №2 и №3 и введите'
              u'результаты измерений в поля длительностей ниже:<br>'
              u'После перехода светодиода №2 в режим постоянного свечения (ПРОДУВ №1) переведите НОПС в требуемое '
              u'положение (установите напротив окна для фотометрирования соответствующий отражающий элемент), если '
              u'необходимо определить меру на первом продуве (указывается в паспорте НОПС). При определении погрешности '
              u'измерения на втором продуве (указывается в паспорте НОПС), не совершая никаких действий, дождитесь '
              u'погасания светодиода №2 и свечения светодиода №3, и теперь переведите НОПС в нужное положение.'
              u'<р>По завершении измерительного процесса (погасание всех светодиодов на панели и выключение побудителя '
              u'расхода газа), выполните команду «ЧТЕНИЕ РЕЗУЛЬТАТА», считайте с экрана полученное значение и полученный '
              u'результат введите в поле ниже. Верните пластину НОПС в исходное положение.',
         conditions=u'deltaC5=((С5-С5р)/С5р) *100',
         params=u'C5 $ t1 $ t2 $ deltaC5',
         param_comments=u'Измеренная экв. концентрация$ Длительность 1-го эксп. продува$ Длительность 2-го эксп. продува',
         param_names=u'C<sub>&lNDEX</sub> $ T<sub> 1 (</sub>&lNDEX<sub>)</sub> $ T<sub>2(</sub>&INDEX<sub>)</sub>',
         param_hints=u'C5p $ 90 $ 90',
         calculation=u'',
         iterations=15, question_type=qtype_value,
         iterparams=u'C5av $ t1av $ t2av $ deltaC5av',
         itercalc=u'C5av=avg(C5); t1av=avg(t1); t2av=avg(t2); deltaC5av=avg(deltaC5)',
         itercond=u'(abs(deltaC5av)<=15) and (89 <= t1av <= 91) and (89 <= t2av <= 91)',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (δ ≤ ±15%, Т=90±1с)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (δ ≤ ±15%. Т=90±1с)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         reportstring=u'<br>4-6 ПДК: T<sub>1</sub>={t1av} с, T<sub>2</sub>={t2av) с, C={C5av} ПДК, δ={deItaC5av}%')
Question(question_group=dt3_gr2, num=5, caption=u'Подготовка к определению погрешности измерения эквивалентных значений '
                                                u'концептраций на 7-9 ПДК',
         text=u'<p> Установите в прибор ДМК-21 один из экземпляров НОПС, типа, соответствующего испытываемому'
              u'измерительному преобразователю, с паспортным значением эквивалентной концентрации от 7ПДК до 9 ПДК.',
         condition=u'х', params=u'х', calculation=u'',
         param_comments=u'Действие выполнено ', iterations=0,
         question_type=qtype_confirm)
Question(question_group=dt3_gr2, num=6, caption=u'Определение погрешности измерения эквивалентных значений '
                                                u'концентраций на 7-9 ПДК',
         text=u'<р>Подайте команду 9 "Включить циклические измерения на старом пятне (ЦИСП)".'
              u'<р>При переходе светодиода №2 на панели измерительного преобразователя ДМК-21 в мигающий режим, '
              u'переведите пластину НОПС с отражающими элементами на половину хода перемещения до следующего элемента на '
              u'время 1 секунду (примерно, до погасания мигающего светодиода) и быстро верните в прежнее положение.'
              u'При выполнении следующих действий секундомером измерьте время свечения светодиодов №2 и №3 и введите'
              u'результаты измерений в поля длительностей ниже:<br>'
              u'После перехода светодиода №2 в режим постоянного свечения (ПРОДУВ №1) переведите НОПС в требуемое '
              u'положение (установите напротив окна для фотометрирования соответствующий отражающий элемент), если '
              u'необходимо определить меру на первом продуве (указывается в паспорте НОПС). При определении погрешности'
              u'необходимо определить меру на первом продуве (указывается в паспорте НОПС). При определении погрешности '
              u'измерения на втором продуве (указывается в паспорте НОПС), не совершая никаких действий, дождитесь '
              u'погасания светодиода №2 и свечения светодиода №3, и теперь переведите НОПС в нужное положение.'
              u'<р>По завершении измерительного процесса (погасание всех светодиодов на панели и выключение побудителя '
              u'расхода газа), выполните команду «ЧТЕНИЕ РЕЗУЛЬТАТА», считайте с экрана полученное значение и полученный '
              u'результат введите в поле ниже. Верните пластину НОПС в исходное положение.',
         condition=u'deltaC8=((С8-С8р)/С8р) *100',
         params=u'C8 $ t1 $ t2 $ deltaC8',
         param_comments=u'Измеренная экв. концентрация$ Длительность 1-го эксп. продува$ Длительность 2-го эксп. продува',
         param_names=u'C<sub>&INDEX</sub> $ T<sub>1(</sub>&INDEX<sub>)</sub> $ T<sub>2(</sub>&INDEX<sub>)</sub>',
         param_hints=u'C8p $ 90 $ 90',
         calculation=u'',
         iterations=15, question_type=qtype_value,
         iterparams=u'C8av $ t1av $ t2av $ deltaC8av',
         itercalc=u'C8av=avg(C8); t1av=avg(t1); t2av=avg(t2); deltaC8av=avg(deltaC8)',
         itercond=u'(abs(deltaC8av)<=15) and (89 <= t1av <= 91) and (89 <= t2av <= 91)',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (δ ≤ ±15%, Т=90 ± 1с)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (δ ≤ ±15%, Т=90 ± 1c)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         reportstring=u'<br>7-9 ПДК: T<sub>1</sub>={t1av) с, T<sub>2</sub>={t2av) с, C={C8av) ПДК, δ={deltaC8av}%')
Question(question_group=dt3_gr3, num=1, caption=u'Определение погрешности расхода газовой смеси',
         text=u'<p>Подключите к входному штуцеру измерительного преобразователя ДМК-21 ротаметр.'
              u'<р>Подайте на измерительный преобразователь ДМК-21 команду "ПРОДУВ".'
              u'<р>Снимите показания ротаметра',
         condition=u'(-10 <= delta <= 15)',
         params=u'R $ delta',
         param_comments=u'Расход газа, л/ч',
         param_names=u'R',
         param_hints=u'60',
         calculation=u'delta=((R-60)/60) *100',
         iterations=0, question_type=qtype_value,
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (δ ≤ +15%/-10%)</i>'
                            u'<br><br>Заключение:<u> Оборудование годно к эксплуатации </u>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (δ ≤ +15%/-10%)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         reportstring=u'<br>Расход: {R} л/ч, δ={delta}%')
## Запросы для групп запросов для типа оборудования devtype4 (ИГ-9)
Question(question_group=dt4_gr0, num=1, caption=u'Измерение параметров окружающей среды',
         text=u'Укажите текущие параметры окружающей среды.',
         condition=u'(15 <= t <= 25) and (84 <=р <= 106,7) and (30 <= h <= 80)', params=u't $ p $ h',
         param_comments=u'Температура, °C $ Давление, кПа $ Отн. влажность воздуха, %',
         param_names=u't $р $ h', param_hints=u'20 $ 100 $ 70', calculation=u'', iterations=0,
         reportstring=u'<br> Температура окружающей среды: {t} °C<br>Давление: {p} кПа'
                      u'<br>Относительная влажность воздуха: {h}%',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничении '
                            u'(Температура: 15 ≤ t ≤ 25 °С; Давление: 84 ≤р≤106,7 кПа; Влажность: от 30% до 80%)</i>',
         conclusion_failure=u'<br><i> Значения лежат за пределами заданных ограничений'
                            u'(Температура: 15 ≤t ≤25 °С; Давление: 84 ≤р≤ 106,7 кПа; Влажность: от 30% до 80%)</i>'
                            u'<br><br> Заключение :<u> Поверка невозможна </u>',
         question_type=qtype_value)
dt4_img1 = Image (name=u'scheme', data=loadImageData ('db_images/ig9_01.jpg'))
Question(question_group=dt4_gr1, num=1, caption=u'Проведение подготовительных действий',
         images=[dt4_img1],
         text=u'<p>1) Выдержите средства поверки и поверяемый прибор до выравнивания их температуры с температурой '
              u'помещения, где производится поверка.'
              u'<р>2) Подготовьте средства поверки к работе в соответствии с их эксплуатационной документацией'
              u'<р>3) Соберите схему поверки в соответствии с рисунком.<p><center><img src="scheme"> </center>'
              u'<p>Примечания:<br> 1. Составные части схемы соединены трубкой 6 х 1,5 ТУ 6-01-1196-79'
              u'<br>2. Измерения параметров прибора проводятся после продувки газовой магистрали соответствующей '
              u'поверочной смесью не менее 10 с при расходе смеси (0,3 ± 0,03) л/мин.',
         condition=u'x and у and z', params=u'x $ у $ z', calculation=u'',
         param_comments=u'Действие №1 выполнено $ Действие №2 выполнено $ Действие №3 выполнено', iterations=0,
         question_type=qtype_confirm)
Question(question_group=dt4_gr2, num=1, caption=u'Установление соответствия требованиям к внешнему виду',
         text=u'<p>Установите соответствие поверяемого прибора следующим требованиям:'
              u'<р>а) комплектность должна соответствовать п. 3.1 руководства по эксплуатации 14-02.02.2.00. 000 РЭ;'
              u'<р>б) сохранность маркировки в течение всего срока службы прибора;'
              u'<р>в) должен быть собран без перекосов и не иметь механических повреждений.'
              u'<р>Допускается наличие царапин на стекле цифрового индикатора и панели прибора глубиной не более 0.1 мм, '
              u'которые не нарушают маркировки и не влияют на работоспособность прибора.',
         condition=u'x and у and z', params=u'x $ у $ z', calculation=u'',
         param_comments=u'Требование №1 выполнено $ Требование №2 выполнено $ Требование №3 выполнено', iterations=0,
         question_type=qtype_confirm,
         conclusion_success=u'<br>Внешний вид соответствует требованиям',
         conclusion_failure=u'<br>Внешний вид не соответствует требованиям'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>')
Question(question_group=dt4_gr3, num=1, сарtion=u'Подготовка к опробованию прибора',
         text=u'<p> 1) Включите прибор нажатием кнопки ВКЛ: на индикаторе должно кратковременно появиться сообщение '
              u'"---". затем погаснуть, и прибор должен перейти в режим измерения по метану с отображением на '
              u'индикаторе значения концентрации объемной доли измеряемого газа, выраженного в процентах, например, '
              u'"METAH 0.25% об. доли".'
              u'<р>2) Прогрейте датчик газа в течение двух минут.'
              u'<р>3) Убедитесь, что показания прибора при отсутствии метана находятся в пределах от 0 до 0.15%. '
              u'При необходимости произведите подстройку нуля.'
              u'<р>4) Произведите установку порогов срабатывания сигнализации по метану - 2.00% и пропану - 0.8% '
              u'в соответствии с п. 6.4 руководства по эксплуатации 14-02.02.2.00.000 РЭ;',
         condition=u'x and у and z and k', params=u'x $ y $ z $ k', calculation=u'',
         param_comments=u'Действие №1 выполнено $ Действие №2 выполнено $ Действие №3 выполнено $'
                        u'Действие №4 выполнено', iterations=0,
         question_type=qtype_confirm)
Question(question_group=dt4_gr3, num=2, caption=u'Опробование прибора',
         text=u'<p>Пoдaйтe в камеру поверочную метано-воздушную смесь 5а. Поместите датчик прибора в камеру. Произведите '
              u'отсчет показаний прибора через 30 с. Укажите показания прибора.'
              u'<р>Прекратите подачу поверочной смеси 5а и извлеките датчик прибора из камеры.',
         condition=u'abs(delta5a) <= 0.25', params=u'c5a $ delta5a', param_names=u'C', param_hints=u'2.5',
         param_comments=u'Результат измерений, %', iterations=0,
         calculation=u'delta5a=c5a-2.5',
         reportstring=u'<br>Смесь 5a. Измеренное значение: {c5a}. Погрешность: (delta5a}%',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (d ≤ ±0.25%)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (d ≤ ±0.25%)<i>'
                            u'<br><br> Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
Question(question_group=dt4_gr3, num=3, caption=u'Опробование прибора',
         text=u'<p>1) Включалась ли прерывистая звуковая и световая сигнализация при подаче смеси в камеру?'
              u'<р>2) Перейдите в режим измерения пропана нажатием кнопки М.П: на индикаторе должно кратковременно '
              u'появиться сообщение "---", погаснуть и опять появиться с отображением на индикаторе значения '
              u'концентрации объемной доли измеряемого газа, выраженного в процентах, например, "ПРОПАН 0.03% об. доли"'
              u'<р>3) Убедитесь, что показания прибора при отсутствии пропана находятся в пределах от 0 до 0.10%.',
         condition=u'x and у and z and k', params=u'x $ у $ z $ k', calculation=u'',
         param_comments=u'Требование п. 1 выполнено $ Действие №2 выполнено $ Действие №3 выполнено', iterations=0,
         conclusion_failure=u'<br>Сигнализация прибора неисправна.'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_confirm)
Question(question_group=dt4_gr3, num=4, caption=u'Опробование прибора',
         text=u'<p>Подайте в камеру смесь 5б. Произведите отсчет показаний прибора через 30 с. Укажите показания '
              u'прибора.',
         condition=u'abs(delta5b) <= 0.1', params=u'c5b $ delta5b', param_names=u'C', param_hints=u'1',
         param_comments=u'Результат измерений, %', iterations=0,
         calculation=u'delta5b=c5b-1',
         reportstring=u'<br>Смесь 5б. Измеренное значение: {c5b}, Погрешность: {delta5b}%',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (d≤±0.1%)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (d ≤±0.1%)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
Question(question_group=dt4_gr3, num=5, caption=u'Опробование прибора',
         text=u'<p>Включалась ли прерывистая звуковая и световая сигнализация при подаче смеси в камеру?',
         condition=u'x', params=u'x', calculation=u'',
         param_comments=u'Требование выполнено', iterations=0,
         conclusion_failure=u'<br> Сигнализация прибора неисправна.'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_confirm)
Question(question_group=dt4_gr4, num=1, caption=u'Определение характеристик',
         text=u'<p>Переведите прибор в режим измерения концентрации метана'
              u'<р>Подайте в камеру смесь За. Поместите датчик прибора в камеру. После установления показаний'
              u'зафиксируйте их значение.'
              u'<р>Подайте в камеру смесь 5а. Поместите датчик прибора в камеру. После установления показаний '
              u'зафиксируйте их значение.'
              u'<р>Переведите прибор в режим измерения концентрации пропана'
              u'<р>Подайте в камеру смесь 3б. Поместите датчик прибора в камеру. После установления показаний '
              u'зафиксируйте их значение.'
              u'<р>Подайте в камеру смесь 5б. Поместите датчик прибора в камеру. После установления показаний '
              u'зафиксируйте их значение.',
         condition=u'(abs(delta3a)<=0.25) and (abs(delta5a)<=0.25) and (abs(delta3b)<=0.1) and (abs(delta5b)<=0.1)',
         params=u'c3a $ c5a $ c3b $ c5b $ delta3a $ delta5a $ delta3b $ delta5b',
         param_names=u'C(3a) $ C(5a) $ C(3б) $ C(5б)', param_hints=u'1 $ 2.5 $ 0.4 $ 1',
         param_comments=u'Концентрация смеси За, % $ Концентрация смеси 5а, % $ '
                        u'Концентрация смеси 3б, % $ Концентрация смеси 5б, %', iterations=0,
         calculation=u'delta3a=c3a-1; delta5a=c5a-2.5; delta3b=c3b-0.4; delta5b=c5b-1',
         reportstring=u'<table border="1"><tr><td>Наименование параметра<td>Заданное значение параметра'
                      u'<td>Измеренное значение параметра<td>Погрешность измерения, %'
                      u'<td>Допускаемая погрешность измерения, %<tr><td colspan="5">Диапазон измерения и допускаемая'
                      u'погрешность<tr><td>-по метану<td>1,00%<td>{c3a}<td>{delta3a}'
                      u'<td>0,25%<tr><td><td>2,50%<td>{c5a}<td>{delta5a}<td>0,25%<tr><td>-по пропану<td> 0,40%<td> {c3b}'
                      u'<td>{delta3b}<td>0,10%<tr><td><td>1,00%<td>{c5b}<td>{delta5b}<td>0,10%',
         conclusion_success=u'<tr><td colspan="5"><i>Значения лежат в пределах заданных ограничений '
                            u'(d ≤ ±0.25% для метана, d ≤ ±0.1% для пропана)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений'
                            u'(d ≤ ±0.25% для метана, d ≤ ±0.1% для пропана)</i></table>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
Question(question_group=dt4_gr4, num=2, caption=u'Определение характеристик',
         text=u'<p>Переведите прибор в режим измерения концентрации метана. Подайте в камеру смесь 5а. Поместите датчик '
              u'прибора в камеру. После стабилизации показаний, удалите датчик прибора из камеры и одновременно'
              u'включите секундомер.'
              u'<р>При достижении показаний 0.25% выключите секундомер. Укажите показания секундомера.'
              u'<р>Поместите датчик прибора в камеру и одновременно включите секундомер.'
              u'<р>При достижении показаний 2.25% выключите секундомер. Укажите показания секундомера.',
         condition=u't00 <= 30',
         params=u't01 $ t09 $ t00',
         param_names=u'т<sub>0,1</sub> $ т<sub>0,9</sub>', param_hints=u'20 $ 20',
         param_comments=u'Время при уменьшении, c $ Время при увеличении, с', iterations=0,
         calculation=u't00=(t01+t09)/2',
         reportstring=u'<tr><td colspan="5">Время установления показаний:<tr><td>т<sub>0.1 </sub><td>-<td>{t01}<td>-'
                      u'<td>-<tr><td>т<sub>0,9</sub><td>-<td>{t09}<td>-<td>-<tr><td>т<td>30 c<td>{t00}'
                      u'<td>-<td>-',
         conclusion_success=u'<tr><td colspan="5"> <i>3начения лежат в пределах заданных ограничений '
                            u'(т ≤ 30 c)</i></table>'
                            u'<br><br>Заключение:<u> Оборудование годно к эксплуатации </u>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений'
                            u'(т ≤ 30 c)</i></table>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)

## Запросы для групп запросов для типа оборудования devtype5 (ИКАР-Л)
Question(question_group=dt5_gr0, num=1, caption=u'Измерение параметров окружающей среды',
         text=u'Укажите текущие параметры окружающей среды.',
         condition=u'(19 <= t <= 21) and (100 <=р <= 103) and (45 <= h <= 75)', params=u't $ p $ h',
         param_comments=u'Температура, °C $ Давление, кПа $ Отн. влажность воздуха, %',
         param_names=u't $ p $ h', param_hints=u'20 $ 100 $ 70', calculation=u'', iterations=0,
         reportstring=u'<br>Температура окружающей среды: {t} °C<br>Давление: {p} кПа'
                      u'<br>Относительная влажность воздуха: {h}%',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений '
                            u'(Температура: 19 ≤ t ≤ 21 °С; Давление: 100 ≤ р ≤ 103 кПа; Влажность: от 45% до 75%)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений'
                            u'(Температура: 19≤t≤21 °С; Давление: 100 ≤р≤103 кПа: Влажность: от 45% до 75%)</i>'
                            u'<br><br>Заключение:<u> Поверка невозможна </u>',
         question_type=qtype_value)
Question(question_group=dt5_gr1, num=1, caption=u'проведение подготовительных действий',
         text=u'<p>Перед проведением поверки баллоны с азотом и ПГС, если они находились на улице в зимнее время, '
              u'необходимо выдержать в помещении, где осуществляется поверка, не менее 1 ч.'
              u'<р>1) Приверните на баллоны редукторы.'
              u'<р>2) В крышку с перфорацией, расположенной в нижней части корпуса газоанализатора, вверните '
              u'ниппель для подачи газовой смеси (из комплекта ЗИП)',
         condition=u'x and у', params=u'x $ у', calculation=u'',
         param_comments=u'Действие №1 выполнено $ Действие №2 выполнено', iterations=0,
         question_type=qtype_confirm)
Question(question_group=dt5_gr2, num=1, caption=u'Установление соответствия требованиям к внешнему виду',
         text=u'<p>Установите соответствие поверяемого прибора следующим требованиям:'
              u'<р>1) на газоанализаторе не должно быть механических повреждений в виде вмятин, царапин и других '
              u'дефектов, влияющих на работоспособность;'
              u'<р>2) маркировка газоанализатора должна соответствовать маркировке, указанной в руководстве по '
              u'эксплуатации;'
              u'<р>3) на газоанализаторе должны находиться и быть неповрежденными пломбы.',
         condition=u'x and у and z', params=u'x $ y $ z', calculation=u'',
         param_comments=u'Требование №1 выполнено $ Требование №2 выполнено $ Требование №3 выполнено', iterations=0,
         question_type=qtype_confirm,
         conclusion_success=u'<br>Внешний вид соответствует требованиям',
         conclusion_failure=u'<br>Внешний вид не соответствует требованиям'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>')
Question(question_group=dt5_gr3, num=1, caption=u'Опробование прибора',
         text=u'<p>Газоанализатор включают в работу нажатием кнопки ВКЛ.'
              u'<р> Через 10 мин. (прогрев) на цифровом индикаторе должно установиться значение содержания кислорода (%)'
              u'(далее — показания газоанализатора) в окружающем воздухе.'
              u'<р>Затем на вход газоанализатора подают смесь № 3.'
              u'Через 5 мин. показания газоанализатора (%) фиксируют и, в случае необходимости, корректируют '
              u'(газоанализатор калибруют): резистором ЧУВСТ. устанавливают на цифровом индикаторе показания '
              u'(%), равные действительному значению содержания кислорода (%) в смеси №3.',
         condition=u'x', params=u'x', calculation=u'',
         param_comments=u'Калибровка произведена', iterations=0,
         question_type=qtype_confirm)
Question(question_group=dt5_gr4, num=1, caption=u'Определение основной абсолютной погрешности',
         text=u'<p>Подайте на вход газоанализатора смесь №1. Через 5 минут зафиксируйте показания газоанализатора.'
              u'<р>Подайте на вход газоанализатора смесь №2. Через 5 минут зафиксируйте показания газоанализатора.'
              u'<р>Подайте на вход газоанализатора смесь №3. Через 5 минут зафиксируйте показания газоанализатора.'
              u'<р>Подайте на вход газоанализатора смесь №2. Через 5 минут зафиксируйте показания газоанализатора.'
              u'<р>Подайте на вход газоанализатора смесь №1. Через 5 минут зафиксируйте показания газоанализатора.'
              u'<р>Подайте на вход газоанализатора смесь №3. Через 5 минут зафиксируйте показания газоанализатора',
         condition=u'abs(delta) <= 0.3 ',
         params=u'p11 $ p21 $ p31 $ p22 $ p12 $ p32 $ delta',
         param_names=u'P1,1 $ P2,1 $ P3,1 $ P2,2 $ P1,2 $ P3,2', param_hints=u'0 $ 12 $ 24 $ 12 $ 0 $ 24',
         param_comments=u'Содерж. O<sub>2</sub> в смеси №1 $ Содерж. O<sub>2</sub> в смеси №2 $'
                        u'Содерж. O<sub>2</sub> в смеси №3 $ Содерж. O<sub>2</sub> в смеси №2 $'
                        u'Содерж. O<sub>2</sub> в смеси №1 $ Содерж. O<sub>2</sub> в смеси №3', iterations=0,
         calculation=u'dmax=max((p11,р21-12,р31-24,р22-12,р12,р32-24)); '
                     u'dmin=min((p11,р21-12,рЗ1-24,р22-12,pl2,р32-24)); delta = dmax if abs(dmax)>abs(dmin) else dmin',
         reportstring=u'<br>Измеренные показания: Смесь №1: {p11}%, {p12}%, эталон: 0%;'
                      u'Смесь №2: {p21}%, {p22}%, эталон: 12%; Смесь №3: {p31}%, {p32}%, эталон: 24%. '
                      u'Максимальное отклонение: {delta)%',
         conclusion_success=u'< br><i> Значения лежат в пределах заданных ограничений '
                            u'(d ≤±0.3%)</i>'
                            u'<br><br>Заключение:<u> Оборудование годно к эксплуатации </u>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений'
                            u'(d ≤ ±0.3%)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)

## Запросы для групп запросов для типа оборудования devtype6 (ИКОНЭТ-МП)
Question(question_group=dt6_gr0, num=1, caption=u'Измерение параметров окружающей среды',
         text=u'Укажите текущие параметры окружающей среды и переменного тока в электросети.',
         condition=u'(15<=t<=25) and (94<=p<=106) and (30<=h<=80) and (198<=u<=242) and (49<=f<=51)',
         params=u't $ p $ h $ u $ f',
         param_comments=u'Температура, °C $ Давление, кПа $ Отн. влажность воздуха, % $ Напряжение, В $ Частота, Гц',
         param_names=u't $ р $ h $ U $ v', param_hints=u'20 $ 100 $ 70 $ 220 $ 50', calculation=u'', iterations=0,
         reportstring=u'<br>TeMnepamypa окружающей среды: {t} °C<br>Давление: {p} кПа'
                      u'<br>Относительная влажность воздуха: {h}%<br>Напряжение питания переменного тока: {u} В'
                      u'<br> Частота переменного тока: {f} Гц',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений '
                            u'(Температура: 20±5 °С; Давление: 100±6 кПа; Влажность: 30%-80%; '
                            u'Напряжение: 220±22 В; Частота: 50±1 Гц)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений'
                            u'(Температура: 20±5 °С; Давление: 100±6 кПа; Влажность: 30%-80%; '
                            u'Напряжение: 220±22 В; Частота: 50±1 Гц)</i>'
                            u'<br><br>Заключение:<u> Поверка невозможна </u>',
         question_type=qtype_value)
Question(question_group=dt6_gr1, num=1, caption=u'Проведение подготовительных действий',
         text=u'<p>1) Приведите спиртомер в рабочее состояние согласно разделу 8 Паспорта.',
         condition=u'x', params=u'x', calculation=u'',
         param_comments=u'Дeйcmвue выполнено', iterations=0,
         question_type=qtype_confirm)
Question(question_group=dt6_gr2, num=1, caption=u'Установление соответствия требованиям к внешнему виду',
         text=u'<р> Установите соответствие поверяемого прибора следующим требованиям:'
              u'<р>1) полная комплектность в соответствие с разделом 4,'
              u'<р>2) четкость всех надписей,'
              u'<р>3) отсутствие механических повреждений,'
              u'<р>4) отсутствие обрывов, изломов сетевого шнура и кабеля.',
         condition=u'x and у and z and k', params=u'x $ y $ z $ k', calculation=u'',
         param_comments=u'Требование №1 выполнено $ Требование №2 выполнено $ Требование №3 выполнено $'
                        u'Требование №4 выполнено', iterations=0,
         question_type=qtype_confirm,
         conclusion_success=u'<br>Внешний вид соответствует требованиям',
         conclusion_failure=u'<br>Внешний вид не соответствует требованиям'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>')
Question(question_group=dt6_gr3, num=1, caption=u'Опробование прибора',
         text=u'<p> Проведите проверку работоспособности спиртомера согласно разделу 8 Паспорта.',
         condition=u'x', params=u'x', calculation=u'',
         param_comments=u'Проверка произведена', iterations=0,
         question_type=qtype_confirm)
Question(question_group=dt6_gr4, num=1, caption=u'Косвенная аттестация опорного канала кюветы',
         text=u'<p> В измерительный канал кюветы залейте водно-спиртовый раствор с крепостью одинаковой или близкой '
              u'к номиналу кюветы (к значению крепости эталонного раствора в опорном канале, приписанному при '
              u'предыдущей поверке). Крепость этого раствора, служащего для сличения, предварительно определите '
              u'эталонным спиртомером 1-го разряда.'
              u'<р> Укажите результат измерения',
         condition=u'True',
         params=u's0',
         param_names=u's<sub>0</sub>', param_hints=u'40', param_comments=u'Крепость раствора', iterations=0,
         calculation=u'',
         question_type=qtype_value)
Question(question_group=dt6_gr4, num=2, caption=u'Косвенная аттестация опорного канала кюветы',
         text=u'<p> Оптическим спиртомером определите крепость водно-спиртового раствора в измерительном канале кюветы.'
              u'<р>Укажите результат измерения',
         condition=u'',
         params=u's',
         param_names=u's<sub> &INDEX</sub>', param_hints=u's0',
         param_comments=u'Крепость раствора', iterations=10,
         calculation=u'',
         iterparams=u'sav $ dsav $ s0 $ DSA',
         itercalc=u'sav=avg(s); dsav=msdev(s); DSA=(sav-s0) ',
         itercond=u'(abs(dsav)<=ds0) and (abs(DSA)<(DS0-0.02))',
         reportstring=u'<br>Кювета номиналом {s0}% об. Предел погрешности dS<sub>A</sub>={DSA}, CKO={dsav}',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (dS<sub>A</sub> '
                            u'и СКО не превышают паспортных значений)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений dS<sub>А</sub> '
                            u'и СКО не превышают паспортных значений)</i>'
                            u'<br><br> Заключение: <u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
Question(question_group=dt6_gr5, num=1, caption=u'Определение предела допускаемой погрешности',
         text=u'<p>B измерительный канал кюветы залейте водно-спиртовый раствор с крепостью 5% об.' \
              u'<р>Оптическим спиртомером определите крепость водно-спиртового раствора в измерительном канале кюветы.'
              u'<р> Укажите результат измерения',
         condition=u'',
         params=u's',
         param_names=u's<sub>&INDEX</sub>',param_hints=u'5',
         param_comments=u'Крепость раствора', iterations=10,
         calculation=u'',
         iterparams=u'sav $ dsav $ s0 $ DSA',
         itercalc=u'sav=avg(s); dsav=msdev(s); DSA=(sav-5) ',
         itercond=u'(abs(dsav)<=ds0) and (abs(DSA)<(DS0-0.02))',
         reportstring=u'<br> Образец крепостью 5% об. Предел погрешности dS<sub>A</sub>={DSA}, CKO={dsav)',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (dS<sub>A</sub> '
                            u'и СКО не превышают паспортных значений)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (dS<sub>A</sub> '
                            u'и СКО не превышают паспортных значений)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
Question(question_group=dt6_gr5, num=2, caption=u'Определение предела допускаемой погрешности',
         text=u'<p>B измерительный канал кюветы залейте водно-спиртовый раствор с крепостью 40% об.'
              u'<р> Оптическим спиртомером определите крепость водно-спиртового раствора в измерительном канале кюветы.'
              u'<р>Укажитерезультат измерения',
         condition=u'',
         params=u'',
         param_names=u's<sub>&INDEX</sub>', param_hints=u'40',
         param_comments=u'Крепость раствора', iterations=10,
         calculation=u'',
         iterparams=u'sav $ dsav $ s0 $ DSA',
         itercalc=u'sav=avg(s); dsav=msdev(s); DSA=(sav-40) ',
         itercond=u'(abs(dsav)<=ds0) and (abs(DSA)<(DS0-0.02))',
         reportstring=u'<br>Образец крепостью 40% об. Предел погрешности dS<sub>A</sub>={DSA}, CKO={dsav}',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (dS<sub>A</sub> '
                            u'и СКО не превышают паспортных значений)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (dS<sub>А</sub> '
                            u'и СКО не превышают паспортных значений)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)
Question(question_group=dt6_gr5, num=3, caption=u'Определение предела допускаемой погрешности',
         text=u'<p>B измерительный канал кюветы залейте водно-спиртовый раствор с крепостью 90% об.'
              u'<р> Оптическим спиртомером определите крепость водно-спиртового раствора в измерительном канале кюветы.'
              u'<р>Укажите результат измерения',
         condition=u'',
         params=u's',
         param_names=u's<sub>&INDEX</sub>', param_hints=u'90',
         param_comments=u'Крепость раствора', iterations=10,
         calculation=u'',
         iterparams=u'sav $ dsav $ s0 $ DSA',
         itercalc=u'sav=avg(s); dsav=msdev(s); DSA=(sav-90) ',
         itercond=u'(abs(dsav)<=ds0) and (abs(DSA)<(DS0-0.02))',
         reportstring=u'<br>Образец крепостью 90% об. Предел погрешности dS<sub>A</sub>={DSA}, CKO={dsav}',
         conclusion_success=u'<br><i>Значения лежат в пределах заданных ограничений (dS<sub>A</sub> '
                            u'и СКО не превышают паспортных значений)</i>'
                            u'<br><br>Заключение:<u> Оборудование годно к эксплуатации </u>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений (dS<sub>A </sub> '
                            u'и СКО не превышают паспортных значений)</i>'
                            u'<br><br>Заключение:<u> Оборудование не годно к эксплуатации </u>',
         question_type=qtype_value)

## Запросы для групп запросов для типа оборудования devtype7 (ИФГ-М)
Question(question_group=dt7_gr0, num=1, caption=u'Измерение параметров окружающей среды',
         text=u'Укажите текущие параметры окружающей среды.',
         condition=u'(15<=t<=25) and (84<=р<=106.6) and (30<=h<=80)',
         params=u't $ p $ h',
         param_comments=u'Температура, °C $ Давление, кПа $ Отн. влажность воздуха, %',
         param_names=u't $р $ h', param_hints=u'20 $ 100 $ 70', calculation=u'', iterations=0,
         reportstring=u'<br>Tемпература окружающей среды: {t} °C<br>Давление: {p} кПа'
                      u'<br>Относительная влажность воздуха: {h}%',
         conelusion_success=u'<br><i>Значения лежат в пределах заданных ограничений '
                            u'(Температура: 20±5 °С; Давление: от 84 до 106,6 кПа; Влажность: 30%-80%)</i>',
         conclusion_failure=u'<br><i>Значения лежат за пределами заданных ограничений '
                            u'(Температура: 20±5 °С; Давление: 84 до 106,6 кПа; Влажность: 30%-80%)</i>'
                            u'<br><br>Заключение:<u> Поверка невозможна </u>',
         question_type=qtype_value)
Question(question_group=dt7_gr1, num=1, caption=u'Установление соответствия требованиям к внешнему виду',
