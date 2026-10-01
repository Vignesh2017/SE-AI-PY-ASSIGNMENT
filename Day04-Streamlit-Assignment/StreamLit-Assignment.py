import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .table-header {
        font-weight: 700;
        padding: 10px 5px;
        border-bottom: 2px solid #d1d5db;
    }

    .table-row {
        padding: 10px 5px;
        border-bottom: 1px solid #e5e7eb;
        min-height: 42px;
    }

    .grade-badge {
        padding: 4px 10px;
        border-radius: 15px;
        font-weight: 600;
        display: inline-block;
    }

    .top-student {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #bbf7d0;
        background-color: #f0fdf4;
    }

    .bottom-student {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #fecaca;
        background-color: #fef2f2;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GRADE CALCULATION
# ============================================================

def calculate_grade(mark):

    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "F"


# ============================================================
# GRADE COLOR
# ============================================================

def grade_color(grade):

    if grade == "A+":
        return "#166534"

    elif grade == "A":
        return "#15803d"

    elif grade == "B":
        return "#2563eb"

    elif grade == "C":
        return "#ca8a04"

    elif grade == "D":
        return "#ea580c"

    return "#dc2626"


# ============================================================
# SESSION STATE
# ============================================================

if "students" not in st.session_state:
    st.session_state.students = []


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎓 Student Grade Manager</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Manage students, calculate grades and monitor class performance.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TOP SECTION
# INPUT LEFT / TABLE RIGHT
# ============================================================

input_col, table_col = st.columns([1, 2.5], gap="large")


# ============================================================
# LEFT - ADD STUDENT
# ============================================================

with input_col:

    st.markdown(
        '<div class="section-title">➕ Add Student</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        student_name = st.text_input(
            "Student Name",
            placeholder="Enter student name"
        )

        mark = st.number_input(
            "Mark",
            min_value=0,
            max_value=100,
            value=0,
            step=1
        )

        add_student = st.button(
            "➕ Add Student",
            use_container_width=True,
            type="primary"
        )


# ============================================================
# ADD STUDENT LOGIC
# ============================================================

if add_student:

    name = student_name.strip()

    if not name:

        st.error("Please enter a student name.")

    elif any(
        student["name"].lower() == name.lower()
        for student in st.session_state.students
    ):

        st.warning(
            f"Student '{name}' already exists."
        )

    else:

        student = {
            "name": name,
            "mark": mark,
            "grade": calculate_grade(mark)
        }

        st.session_state.students.append(student)

        st.success(
            f"✅ {name} added successfully!"
        )

        st.rerun()


# ============================================================
# RIGHT - STUDENT TABLE
# ============================================================

with table_col:

    st.markdown(
        '<div class="section-title">👨‍🎓 Student Results</div>',
        unsafe_allow_html=True
    )

    students = st.session_state.students

    if students:

        # ----------------------------------------------------
        # SEARCH / SORT / FILTER
        # ----------------------------------------------------

        search_col, sort_col, filter_col = st.columns(
            [2, 1.5, 1.5]
        )

        with search_col:

            search_text = st.text_input(
                "🔎 Search",
                placeholder="Student name...",
                label_visibility="collapsed"
            )

        with sort_col:

            sort_option = st.selectbox(
                "Sort",
                [
                    "Name",
                    "Mark: High → Low",
                    "Mark: Low → High",
                    "Grade"
                ],
                label_visibility="collapsed"
            )

        with filter_col:

            grade_filter = st.selectbox(
                "Filter",
                [
                    "All",
                    "A+",
                    "A",
                    "B",
                    "C",
                    "D",
                    "F"
                ],
                label_visibility="collapsed"
            )


        # ----------------------------------------------------
        # FILTER
        # ----------------------------------------------------

        filtered_students = students

        if search_text:

            filtered_students = [
                student
                for student in filtered_students
                if search_text.lower()
                in student["name"].lower()
            ]


        if grade_filter != "All":

            filtered_students = [
                student
                for student in filtered_students
                if student["grade"] == grade_filter
            ]


        # ----------------------------------------------------
        # SORT
        # ----------------------------------------------------

        if sort_option == "Name":

            filtered_students = sorted(
                filtered_students,
                key=lambda student:
                student["name"].lower()
            )

        elif sort_option == "Mark: High → Low":

            filtered_students = sorted(
                filtered_students,
                key=lambda student:
                student["mark"],
                reverse=True
            )

        elif sort_option == "Mark: Low → High":

            filtered_students = sorted(
                filtered_students,
                key=lambda student:
                student["mark"]
            )

        elif sort_option == "Grade":

            grade_order = {
                "A+": 1,
                "A": 2,
                "B": 3,
                "C": 4,
                "D": 5,
                "F": 6
            }

            filtered_students = sorted(
                filtered_students,
                key=lambda student:
                grade_order[student["grade"]]
            )


        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        with st.container(border=True):

            header = st.columns(
                [3, 1.5, 1.5, 0.8]
            )

            with header[0]:
                st.markdown(
                    '<div class="table-header">'
                    'Student Name'
                    '</div>',
                    unsafe_allow_html=True
                )

            with header[1]:
                st.markdown(
                    '<div class="table-header">'
                    'Mark'
                    '</div>',
                    unsafe_allow_html=True
                )

            with header[2]:
                st.markdown(
                    '<div class="table-header">'
                    'Grade'
                    '</div>',
                    unsafe_allow_html=True
                )

            with header[3]:
                st.markdown(
                    '<div class="table-header">'
                    'Action'
                    '</div>',
                    unsafe_allow_html=True
                )


            # ------------------------------------------------
            # ROWS
            # ------------------------------------------------

            if filtered_students:

                for index, student in enumerate(
                    filtered_students
                ):

                    row = st.columns(
                        [3, 1.5, 1.5, 0.8]
                    )

                    with row[0]:

                        st.markdown(
                            f'<div class="table-row">'
                            f'👤 {student["name"]}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    with row[1]:

                        st.markdown(
                            f'<div class="table-row">'
                            f'{student["mark"]}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    with row[2]:

                        color = grade_color(
                            student["grade"]
                        )

                        st.markdown(
                            f'<div class="table-row">'
                            f'<span class="grade-badge" '
                            f'style="color:{color};">'
                            f'{student["grade"]}'
                            f'</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    with row[3]:

                        if st.button(
                            "🗑️",
                            key=f"delete_{index}_{student['name']}"
                        ):

                            st.session_state.students.remove(
                                student
                            )

                            st.rerun()

            else:

                st.info(
                    "No students match the selected "
                    "search/filter."
                )

    else:

        st.info(
            "No students added yet. "
            "Use the form on the left."
        )


# ============================================================
# CLASS STATISTICS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Class Statistics</div>',
    unsafe_allow_html=True
)


students = st.session_state.students


if students:

    # --------------------------------------------------------
    # BASIC STATISTICS
    # --------------------------------------------------------

    marks = [
        student["mark"]
        for student in students
    ]

    total_students = len(students)

    average_mark = sum(marks) / total_students

    highest_mark = max(marks)

    lowest_mark = min(marks)


    highest_student = next(
        student["name"]
        for student in students
        if student["mark"] == highest_mark
    )


    lowest_student = next(
        student["name"]
        for student in students
        if student["mark"] == lowest_mark
    )


    # --------------------------------------------------------
    # STATISTICS CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👨‍🎓 Total Students",
            total_students
        )

    with col2:

        st.metric(
            "📊 Average Mark",
            f"{average_mark:.2f}"
        )

    with col3:

        st.metric(
            "🏆 Highest Mark",
            highest_mark
        )

    with col4:

        st.metric(
            "📉 Lowest Mark",
            lowest_mark
        )


    # --------------------------------------------------------
    # TOP / LOWEST STUDENT
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.success(
            f"🏆 **Top Student:** {highest_student}  \n"
            f"Mark: **{highest_mark}**"
        )


    with col2:

        if lowest_mark < 50:

            st.error(
                f"⚠️ **Lowest Student:** {lowest_student}  \n"
                f"Mark: **{lowest_mark}**"
            )

        else:

            st.info(
                f"📉 **Lowest Student:** {lowest_student}  \n"
                f"Mark: **{lowest_mark}**"
            )


    # --------------------------------------------------------
    # GRADE DISTRIBUTION
    # --------------------------------------------------------

    st.subheader("🏅 Grade Distribution")


    grade_counts = {
        "A+": 0,
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
        "F": 0
    }


    for student in students:

        grade_counts[
            student["grade"]
        ] += 1


    grade_columns = st.columns(6)


    for index, grade in enumerate(
        grade_counts
    ):

        with grade_columns[index]:

            st.metric(
                grade,
                grade_counts[grade]
            )


    # --------------------------------------------------------
    # PASS / FAIL
    # --------------------------------------------------------

    pass_count = sum(
        1
        for student in students
        if student["mark"] >= 50
    )

    fail_count = total_students - pass_count


    col1, col2 = st.columns(2)


    with col1:

        st.success(
            f"✅ Passing Students: **{pass_count}**"
        )


    with col2:

        if fail_count > 0:

            st.error(
                f"❌ Failing Students: **{fail_count}**"
            )

        else:

            st.success(
                "🎉 All students passed!"
            )


    # --------------------------------------------------------
    # CLEAR ALL
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "🗑️ Clear All Students",
        use_container_width=True
    ):

        st.session_state.students = []

        st.rerun()


else:

    st.info(
        "📊 Class statistics will appear here "
        "after adding students."
    )
