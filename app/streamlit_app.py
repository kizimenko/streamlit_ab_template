import streamlit as st

st.set_page_config(
    page_title="AB Test Description Generator",
    page_icon="",
)

def get_next_file_index():
    import os
    counter_file = "counter.txt"

    # Если файл счетчика не существует, создайте его
    if not os.path.isfile(counter_file):
        with open(counter_file, "w") as file:
            file.write("0")

    # Читайте значение счетчика
    with open(counter_file, "r") as file:
        index = int(file.read())

    # Увеличьте счетчик и сохраните его обратно в файл
    with open(counter_file, "w") as file:
        file.write(str(index + 1))

    return index

def save_to_file(content, file_name_prefix):
    index = get_next_file_index()
    file_name = f"files/{file_name_prefix}_{index}.md"
    with open(file_name, 'w') as file:
        file.write(content)
    return file_name

# Функция для создания ссылки на скачивание файла
def create_download_link(filename, content):
        import base64
        b64 = base64.b64encode(content.encode()).decode()  # некоторые строки <-> bytes преобразования нужны
        return f'<a href="data:text/plain;base64,{b64}" download="{filename}">Скачать описание теста</a>'


def load_from_file():
    uploaded_file = st.file_uploader("Choose a file", type="md")
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        content_dict = parse_file_content(content)
        return content_dict

def parse_file_content(content):
    lines = content.split("\n")
    fields = {}
    current_field = None
    for line in lines:
        if line.startswith("# "):
            current_field = line[2:]
            fields[current_field] = ""
        elif current_field is not None:
            fields[current_field] += line + "\n"
    return fields

def get_user_input():
    st.title("Описание Идеи A/B теста")
    # content_dict = load_from_file()
    # if content_dict is None:
    #     content_dict = {}
    col1, col2 = st.columns(2)
    
    with col1:
        projects = st.text_input("Подразделение", "")
    with col2:
        telegram = st.text_input("Телеграм автора", "")
        
        
    with st.expander("Гипотеза:"):
        st.subheader("Описание проблемы и цели теста:")
        test_goal = st.text_area("Здесь описывается основная цель и проблема которую планируем решить", value="Цель Теста:",
                                help="Опишите, что вы хотите достичь с помощью этого теста. Это может быть увеличение конверсии, улучшение вовлеченности пользователей, снижение оттока и т.д.",
                                placeholder="Опишите, что вы хотите достичь с помощью этого теста. Это может быть увеличение конверсии, улучшение вовлеченности пользователей, снижение оттока и т.д."
                            )
        st.subheader("Как будем решать:")
        idea_desc = st.text_area("Введите описание идеи", "", 
                                placeholder='Опишите, какие изменения вы предлагаете ввести в тестовой группе. Например, это может быть изменение дизайна кнопки, изменение текста на странице и т.д.'
                                )
        st.subheader("Гипотеза:")
        hypothesis = st.text_area("Введите гипотезу", "",
                              placeholder="""Укажите свои предположения о том, как предложенные изменения повлияют на пользовательское поведение. Например: "Предполагается, что изменение цвета кнопки на более яркий приведет к увеличению кликабельности"."""
                              )
        st.subheader("Метрики для анализа:")
        metrics = st.text_area("Метрики на которые мы стараемся повлиять и на которые не хотелось бы влиять", "",
                           placeholder=' Перечислите метрики, по которым будет оцениваться результат теста. Это может быть конверсия, среднее время на сайте, частота кликов и т.д.'
                           )
    with st.expander("Предварительный Анализ:"):    
        st.subheader("Предварительный Анализ:")
        preliminary_analysis = st.text_area("Если были исследования или беглый ресерч то описать", "",
                                            placeholder='Если уже есть какие то исследования или анализы, которые могут помочь в проведении теста, то опишите их здесь.'
                                            )

    with st.expander("Дизайн Теста:"):
        st.subheader("Варианты Теста:")
        test_variants = st.text_area("Введите варианты теста", "", 
                                    placeholder='Опишите варианты, для примера есть 2 варианта - А (контрольный, текущий дизайн или функционал) и B (тестовый, где применяются предложенные изменения).'
                                    )

        st.subheader("Сегментация/Аудитория:")
        segmentation = st.text_area("На какую группу пользователей направлено изменение", "",
                                    placeholder='Если вы планируете тестировать изменения на определенной группе пользователей, укажите критерии для этой сегментации.'
                                    )

        
        st.subheader("Период проведения теста:")
        test_period = st.text_area("Введите период проведения теста", "",
                                placeholder='Укажите период когда хотелось бы запустить тест и на какой период планируется его проведение.'
                                )
    with st.expander("Дополнительная информация:"):
        st.subheader("Сырые Данные:")
        raw_data = st.text_area("Введите информацию о сырых данных", "",
                                placeholder='Укажите, где хранятся сырые данные теста. Это может быть ссылка на облачное хранилище, базу данных и т.д.' 
                                )
        devs = st.checkbox('Требуется привлечение разработки?')
        design = st.checkbox('Требуется привлечение дизайнеров?')
        

    st.header('Оценка идеи по методологии ICE')
    st.markdown("""- Impact (Влияние): Как сильно идея может повлиять на метрики, которые вы пытаетесь улучшить.
- Confidence (Уверенность): Как уверены вы в своих оценках влияния и усилий.
- Ease (Простота): Как много усилий потребуется для реализации идеи.
                """)
    col11, col22, col33 = st.columns(3)
    with col11:
        impact_description = [
            '1 - Низкое влияние',
            '2 - Умеренное влияние',
            '3 - Среднее влияние',
            '4 - Высокое влияние',
            '5 - Очень высокое влияние'
        ]
        impact = st.selectbox('Impact (Влияние)', impact_description, help='Укажите, насколько изменения повлияют на пользовательское поведение')

    with col22:
        confidence_description = [
            '1 - Низкая уверенность',
            '2 - Умеренная уверенность',
            '3 - Средняя уверенность',
            '4 - Высокая уверенность',
            '5 - Очень высокая уверенность'
        ]
        confidence = st.selectbox('Confidence (Уверенность)', confidence_description, help='Укажите, насколько вы уверены в том, что изменения повлияют на пользовательское поведение')

    with col33:
        ease_description = [
            '1 - Очень сложно',
            '2 - Сложно',
            '3 - Средне',
            '4 - Легко',
            '5 - Очень легко'
        ]
        ease = st.selectbox('Ease (Легкость реализации)', ease_description, help='Укажите, насколько легко реализовать изменения')

    ice_score = round(((int(impact[0]) + int(confidence[0]) + int(ease[0])) / 3 ))
    st.markdown(f"### ICE Score: {ice_score}")
    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')
    # st.header("Расчеты:")
    # calculations = st.text_area("Введите информацию о расчетах", "")

    # st.header("Выводы:")
    # conclusions = st.text_area("Введите информацию о выводах", "")

    # st.header("Рекомендации:")
    # recommendations = st.text_area("Введите рекомендации", "")

        

    
    

    

    

    # Создание ссылки на скачивание файла
    if st.button("Сохранить"):
        st.text("\n\n\n\n\n")
        content = (f"Подразделение: {projects}, Телеграм автора: {telegram}\n\n"
                    "## Описание Идеи A/B теста\n\n"
                    "### Цель Теста:\n" + test_goal + "\n\n"
                    "### Описание идеи:\n" + idea_desc + "\n\n"
                    "### Предварительный Анализ:\n" + preliminary_analysis + "\n\n"
                    "## Гипотеза:\n" + hypothesis + "\n\n"
                    "## Дизайн Теста\n\n"
                    "### Варианты Теста:\n" + test_variants + "\n\n"
                    "### Метрики для анализа:\n" + metrics + "\n\n"
                    "### Сегментация:\n" + segmentation + "\n\n"
                    "### Период проведения теста:\n" + test_period + "\n\n"
                    "## Результаты\n\n"
                    "### Сырые Данные:\n" + raw_data + "\n\n"
                    "### Оценка идеи\n\n" + f"\nTotal: {ice_score} \n - impact: {impact[0]} \n - confidence: {confidence[0]} \n - ease: {ease[0]} \n\n"
                )


        file_name = save_to_file(content, "ab_description")

        st.success("Ваше описание теста успешно сохранено.")
        st.markdown(create_download_link(file_name, content), unsafe_allow_html=True)


get_user_input()