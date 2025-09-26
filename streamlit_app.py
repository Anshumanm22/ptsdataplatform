# streamlit_pts_demo.py
# Run with: streamlit run streamlit_pts_demo.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

users = {
    "admin": {"password": "admin123", "role": "admin", "name": "System Administrator"},
    "teacher": {"password": "teacher123", "role": "teacher", "name": "Teacher"},
    "coordinator": {"password": "coord123", "role": "coordinator", "name": "Center Coordinator"}
}

def authenticate():
    st.title("PTS Platform Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if username in users and users[username]["password"] == password:
                st.session_state["authenticated"] = True
                st.session_state["user"] = username
                st.session_state["role"] = users[username]["role"]
                st.session_state["user_name"] = users[username]["name"]
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        # Show demo credentials
        with st.expander("Demo Credentials"):
            st.write("**Admin:** admin / admin123")
            st.write("**Teacher:** teacher / teacher123") 
            st.write("**Coordinator:** coordinator / coord123")

if "authenticated" not in st.session_state:
    authenticate()
    st.stop()

with st.sidebar:
    st.write(f"Logged in as: **{st.session_state['user_name']}**")
    st.write(f"Role: {st.session_state['role'].title()}")
    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Page config
st.set_page_config(
    page_title="PTS Data Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .student-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-granted {
        background-color: #d4edda;
        color: #155724;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .status-review {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'students_data' not in st.session_state:
    st.session_state.students_data = pd.DataFrame({
        'name': ['Ananya Chakrabory', 'Rahul Mondal', 'Priya Das', 'Amit Kumar', 'Sneha Roy'],
        'grade': [9, 10, 9, 10, 9],
        'age': [14, 15, 14, 15, 14],
        'center': ['Saltlake Center'] * 5,
        'scholarship_status': ['Active', 'Active', 'Active', 'Under Review', 'Active'],
        'entry_score': [24, 23, 26, 21, 25],
        'mid_year_math': [82, 78, 88, 75, 80],
        'mid_year_english': [75, 70, 83, 72, 78],
        'mid_year_science': [80, 74, 87, 79, 82],
        'end_year_math': [85, 80, 90, 78, 83],
        'end_year_english': [78, 72, 85, 75, 80],
        'end_year_science': [82, 76, 88, 80, 85],
        'attendance_mid': [94, 91, 96, 88, 92],
        'attendance_end': [95, 93, 97, 85, 94],
        'continuation_approved': [None, 'Approved', None, 'Pending', None],
        'teacher_assigned': ['Teacher A', 'Teacher B', 'Teacher A', 'Teacher C', 'Teacher A']
    })

if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# Calculate academic scores
def calculate_academic_score(row):
    subjects = ['english', 'bengali', 'math', 'science', 'social']
    avg = row[subjects].mean()
    return round(avg, 1)

# Add academic score column
st.session_state.students_data['academic_avg'] = st.session_state.students_data.apply(calculate_academic_score, axis=1)

# Header
st.markdown("""
<div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🎓 Peerless Trinity Scholarship</h1>
    <p style='color: white; margin: 0; font-size: 1.2rem; opacity: 0.9;'>Data Management Platform - Live Demo</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Platform Controls")


# Navigation

if st.session_state["role"] == "admin":
    page_options = ["Dashboard Overview", "Student Details", "Scholarship Approvals", "Reports & Analytics"]
elif st.session_state["role"] == "teacher":
    page_options = ["Dashboard Overview", "Student Details", "Data Entry"]
else:  # coordinator
    page_options = ["Dashboard Overview", "Reports & Analytics"]

page = st.sidebar.selectbox("Select Page", page_options)

# Success message
if st.session_state.show_success:
    st.success("✅ Student data saved successfully!")
    st.session_state.show_success = False

# Dashboard Overview Page
# Dashboard Overview Page
if page == "Dashboard Overview":
    
    if st.session_state["role"] == "admin":
        st.header("🏢 Admin Dashboard - Multi-Center Overview")
        
        # Mock multi-center data
        center_data = pd.DataFrame({
            'center': ['Saltlake Center', 'Park Street Center', 'Howrah Center', 'New Town Center'],
            'total_students': [25, 18, 22, 15],
            'avg_attendance': [92.5, 89.2, 94.1, 87.8],
            'scholarships': [18, 12, 16, 10],
            'avg_score': [24.2, 23.1, 25.4, 22.8]
        })
        
        # Multi-center metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Centers", len(center_data), delta="Active")
        with col2:
            st.metric("Total Students", center_data['total_students'].sum(), delta="All Centers")
        with col3:
            st.metric("Total Scholarships", center_data['scholarships'].sum(), delta="Granted")
        with col4:
            st.metric("Network Avg Score", f"{center_data['avg_score'].mean():.1f}/30", delta="System-wide")
        
        # Center comparison table
        st.subheader("📊 Center Performance Comparison")
        st.dataframe(center_data, use_container_width=True, hide_index=True)
        
        # Center selector for detailed view
        selected_center = st.selectbox("View Center Details:", center_data['center'].tolist())
        center_students = st.session_state.students_data[st.session_state.students_data['center'] == selected_center]
        
        if len(center_students) > 0:
            st.subheader(f"Students at {selected_center}")
            st.dataframe(center_students[['name', 'grade', 'attendance', 'total_score', 'status']], 
                        use_container_width=True, hide_index=True)
    
    elif st.session_state["role"] == "teacher":
        st.header("👩‍🏫 Teacher Dashboard - My Students")
        
        # Mock teacher assignment (in real app, this would be from database)
        teacher_students = st.session_state.students_data.sample(n=3)  # Simulate assigned students
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("My Students", len(teacher_students), delta="Assigned")
        with col2:
            st.metric("Avg Attendance", f"{teacher_students['attendance'].mean():.1f}%", delta="My Class")
        with col3:
            st.metric("Scholarships", len(teacher_students[teacher_students['status'] == 'Scholarship Granted']), delta="Achieved")
        
        st.subheader("📚 My Assigned Students")
        
        # Detailed student cards for teacher
        for idx, student in teacher_students.iterrows():
            with st.expander(f"👤 {student['name']} - Grade {student['grade']}", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**Attendance:** {student['attendance']}%")
                with col2:
                    st.write(f"**Academic Avg:** {student['academic_avg']:.1f}%")
                with col3:
                    st.write(f"**Total Score:** {student['total_score']}/30")
                with col4:
                    st.write(f"**Status:** {student['status']}")
                
                # Subject breakdown
                subjects = ['English', 'Bengali', 'Math', 'Science', 'Social']
                scores = [student['english'], student['bengali'], student['math'], student['science'], student['social']]
                subject_df = pd.DataFrame({'Subject': subjects, 'Score': scores})
                st.bar_chart(subject_df.set_index('Subject'))
    
    elif st.session_state["role"] == "coordinator":
        st.header("🏛️ Coordinator Dashboard - Center Management")
        
        # Center-specific data (mock single center)
        my_center = "Saltlake Center"
        center_students = st.session_state.students_data[st.session_state.students_data['center'] == my_center]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Center Students", len(center_students), delta=my_center)
        with col2:
            st.metric("Avg Attendance", f"{center_students['attendance'].mean():.1f}%", delta="Center Average")
        with col3:
            st.metric("Scholarships", len(center_students[center_students['status'] == 'Scholarship Granted']), delta="This Center")
        with col4:
            st.metric("At-Risk Students", len(center_students[center_students['total_score'] < 24]), delta="Need Support")
        
        # Grade-wise breakdown
        st.subheader("📊 Grade-wise Performance")
        grade_stats = center_students.groupby('grade').agg({
            'attendance': 'mean',
            'total_score': 'mean',
            'name': 'count'
        }).round(1)
        grade_stats.columns = ['Avg Attendance', 'Avg Score', 'Student Count']
        st.dataframe(grade_stats, use_container_width=True)
        
        # Student overview table
        st.subheader("👥 All Center Students")
        display_data = center_students[['name', 'grade', 'attendance', 'total_score', 'status']].copy()
        display_data.columns = ['Name', 'Grade', 'Attendance %', 'Total Score', 'Status']
        st.dataframe(display_data, use_container_width=True, hide_index=True)
        
        # Action items
        st.subheader("⚠️ Attention Required")
        at_risk = center_students[center_students['attendance'] < 90]
        if len(at_risk) > 0:
            st.warning(f"{len(at_risk)} students have attendance below 90%")
            st.dataframe(at_risk[['name', 'grade', 'attendance']], hide_index=True)
        else:
            st.success("All students maintaining good attendance!")

# Student Details Page
elif page == "Student Details":
    st.header("👤 Student Detail View")
    
    if 'selected_student' not in st.session_state:
        st.info("Select a student from the Dashboard to view details")
        
        # Student selector
        student_names = st.session_state.students_data['name'].tolist()
        selected_name = st.selectbox("Or select a student here:", ["Choose a student..."] + student_names)
        
        if selected_name != "Choose a student...":
            selected_row = st.session_state.students_data[st.session_state.students_data['name'] == selected_name].iloc[0]
            st.session_state.selected_student = selected_row.to_dict()
            st.rerun()
    
    else:
        student = st.session_state.selected_student
        
        # Student Header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"## {student['name']}")
            st.caption(f"Grade {student['grade']} • {student['center']}")
        
        with col2:
            status_color = "🟢" if student['status'] == 'Scholarship Granted' else "🟡"
            st.markdown(f"{status_color} **{student['status']}**")
        
        with col3:
            if st.button("← Back to Dashboard"):
                del st.session_state.selected_student
                st.rerun()
        
        # Score Breakdown
        st.subheader("📊 Score Breakdown")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate component scores (simplified)
        attendance_score = 10 if student['attendance'] >= 95 else (9 if student['attendance'] >= 90 else 8)
        academic_score = int(student['academic_avg'] / 10) if student['academic_avg'] >= 70 else 6
        
        with col1:
            st.metric("Attendance Score", f"{attendance_score}/10", delta=f"{student['attendance']}%")
        
        with col2:
            st.metric("Academic Score", f"{academic_score}/10", delta=f"{student['academic_avg']:.1f}%")
        
        with col3:
            st.metric("Aptitude Score", f"{student['aptitude_score']}/10")
        
        with col4:
            st.metric("Total Score", f"{student['total_score']}/30", 
                     delta="Eligible" if student['total_score'] >= 24 else "Under Review")
        
        # Progress Chart
        col1, col2 = st.columns(2)
        
        with col1:
            # Subject Performance
            subjects = ['English', 'Bengali', 'Math', 'Science', 'Social']
            scores = [student['english'], student['bengali'], student['math'], student['science'], student['social']]
            
            fig_subjects = px.bar(
                x=subjects, 
                y=scores,
                title=f"{student['name']} - Subject Performance",
                color=scores,
                color_continuous_scale='viridis'
            )
            fig_subjects.update_layout(showlegend=False)
            st.plotly_chart(fig_subjects, use_container_width=True)
        
        with col2:
            # Mock Progress Over Time
            months = ['April', 'May', 'June', 'July']
            base_score = student['academic_avg']
            progress_scores = [base_score-5, base_score-3, base_score-1, base_score]
            
            fig_progress = px.line(
                x=months, 
                y=progress_scores,
                title=f"{student['name']} - Progress Over Time",
                markers=True
            )
            fig_progress.update_traces(line_color='#667eea', line_width=3)
            st.plotly_chart(fig_progress, use_container_width=True)
        
        # Generate Report Button
        if st.button("📄 Generate Student Report", type="primary"):
            with st.spinner("Generating report..."):
                import time
                time.sleep(2)  # Simulate processing
                
                st.success("✅ Report generated successfully!")
                st.download_button(
                    label="📥 Download PDF Report",
                    data=f"Student Report for {student['name']} - Generated on {datetime.now().strftime('%Y-%m-%d')}",
                    file_name=f"{student['name']}_report.txt",
                    mime="text/plain"
                )

# Data Entry Page
elif page == "Data Entry":
    st.header("📝 Student Data Entry")
    
    with st.form("student_entry_form", clear_on_submit=True):
        st.subheader("Enter New Student Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Student Name *", placeholder="Enter full name")
            new_grade = st.selectbox("Grade *", [9, 10])
            new_attendance = st.slider("Attendance %", 0, 100, 85)
        
        with col2:
            new_center = st.selectbox("Center", ["Saltlake Center", "Park Street Center", "Howrah Center"])
            new_age = st.number_input("Age", 13, 17, 14 if new_grade == 9 else 15)
        
        st.subheader("Subject Scores")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            new_english = st.number_input("English", 0, 100, 75)
        with col2:
            new_bengali = st.number_input("Bengali", 0, 100, 75)
        with col3:
            new_math = st.number_input("Mathematics", 0, 100, 75)
        with col4:
            new_science = st.number_input("Science", 0, 100, 75)
        with col5:
            new_social = st.number_input("Social Studies", 0, 100, 75)
        
        # Auto-calculate scores
        if st.form_submit_button("💾 Save Student Data", type="primary"):
            if new_name:
                # Calculate scores
                academic_avg = np.mean([new_english, new_bengali, new_math, new_science, new_social])
                attendance_score = 10 if new_attendance >= 95 else (9 if new_attendance >= 90 else 8)
                academic_score = int(academic_avg / 10) if academic_avg >= 70 else 6
                aptitude_score = np.random.randint(6, 10)  # Random for demo
                total_score = attendance_score + academic_score + aptitude_score
                status = "Scholarship Granted" if total_score >= 24 else "Under Review"
                
                # Add new student to dataframe
                new_student = {
                    'name': new_name,
                    'grade': new_grade,
                    'age': new_age,
                    'center': new_center,
                    'attendance': new_attendance,
                    'english': new_english,
                    'bengali': new_bengali,
                    'math': new_math,
                    'science': new_science,
                    'social': new_social,
                    'aptitude_score': aptitude_score,
                    'total_score': total_score,
                    'status': status,
                    'academic_avg': academic_avg
                }
                
                # Add to session state
                st.session_state.students_data = pd.concat([
                    st.session_state.students_data, 
                    pd.DataFrame([new_student])
                ], ignore_index=True)
                
                st.session_state.show_success = True
                st.rerun()
            else:
                st.error("Please enter student name")
    # Admin Approval Page
elif page == "Scholarship Approvals":
    if st.session_state["role"] != "admin":
        st.error("Access Denied: Only admins can approve scholarship continuations")
        st.stop()
    
    st.header("Admin Panel - Scholarship Continuation Approvals")
    
    # Filter Grade 9 students who need continuation approval
    grade_9_students = st.session_state.students_data[
        (st.session_state.students_data['grade'] == 9) & 
        (st.session_state.students_data['continuation_approved'].isna())
    ]
    
    if len(grade_9_students) == 0:
        st.success("No pending approval requests")
    else:
        st.subheader("Pending Approvals for Grade 9 → Grade 10 Continuation")
        
        for idx, student in grade_9_students.iterrows():
            with st.expander(f"Review: {student['name']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Performance Summary**")
                    st.write(f"Entry Score: {student['entry_score']}/30")
                    st.write(f"Mid-Year Avg: {(student['mid_year_math'] + student['mid_year_english'] + student['mid_year_science'])/3:.1f}%")
                    st.write(f"End-Year Avg: {(student['end_year_math'] + student['end_year_english'] + student['end_year_science'])/3:.1f}%")
                
                with col2:
                    st.write("**Attendance**")
                    st.write(f"Mid-Year: {student['attendance_mid']}%")
                    st.write(f"End-Year: {student['attendance_end']}%")
                    
                with col3:
                    st.write("**Recommendation**")
                    end_avg = (student['end_year_math'] + student['end_year_english'] + student['end_year_science'])/3
                    if end_avg >= 75 and student['attendance_end'] >= 90:
                        st.success("Recommended for Continuation")
                    elif end_avg >= 70 and student['attendance_end'] >= 85:
                        st.warning("Conditional Continuation")
                    else:
                        st.error("At Risk - Review Required")
                
                # Approval buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"✅ Approve", key=f"approve_{idx}"):
                        st.session_state.students_data.loc[idx, 'continuation_approved'] = 'Approved'
                        st.success(f"Approved continuation for {student['name']}")
                        st.rerun()
                
                with col2:
                    if st.button(f"❌ Reject", key=f"reject_{idx}"):
                        st.session_state.students_data.loc[idx, 'continuation_approved'] = 'Rejected'
                        st.error(f"Rejected continuation for {student['name']}")
                        st.rerun()
                
                with col3:
                    if st.button(f"⏸️ Hold", key=f"hold_{idx}"):
                        st.session_state.students_data.loc[idx, 'continuation_approved'] = 'On Hold'
                        st.warning(f"Put {student['name']} on hold")
                        st.rerun()

    
    # Preview calculation
    if st.button("🧮 Preview Score Calculation"):
        with st.expander("Score Calculation Preview", expanded=True):
            if 'new_english' in locals():
                academic_avg = np.mean([new_english, new_bengali, new_math, new_science, new_social])
                attendance_score = 10 if new_attendance >= 95 else (9 if new_attendance >= 90 else 8)
                academic_score = int(academic_avg / 10) if academic_avg >= 70 else 6
                aptitude_score = 8  # Example
                total_score = attendance_score + academic_score + aptitude_score
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Attendance Score", f"{attendance_score}/10")
                with col2:
                    st.metric("Academic Score", f"{academic_score}/10")
                with col3:
                    st.metric("Aptitude Score", f"{aptitude_score}/10")
                with col4:
                    st.metric("Predicted Total", f"{total_score}/30")
                
                status = "Scholarship Granted" if total_score >= 24 else "Under Review"
                st.info(f"Predicted Status: **{status}**")

# Analytics & Reports Page
elif page == "Analytics & Reports":
    st.header("📈 Analytics & Reports")
    
    # Report Generation Section
    st.subheader("📄 Generate Custom Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        report_type = st.selectbox("Report Type", [
            "Student Performance Summary",
            "Attendance Analysis",
            "Scholarship Eligibility Report",
            "Center-wise Comparison",
            "Subject-wise Analysis"
        ])
    
    with col2:
        grade_filter_report = st.selectbox("Grade Filter", ["All Grades", "Grade 9", "Grade 10"])
    
    with col3:
        date_range = st.selectbox("Time Period", [
            "Current Month",
            "Last 3 Months",
            "Academic Year 2025-26",
            "Custom Range"
        ])
    
    if st.button("🚀 Generate Report", type="primary"):
        with st.spinner("Generating comprehensive report..."):
            import time
            time.sleep(3)  # Simulate processing
            
            st.success("✅ Report generated successfully!")
            
            # Mock report data
            report_data = f"""
            {report_type}
            Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Filter Applied: {grade_filter_report}
            Time Period: {date_range}
            
            Total Students Analyzed: {len(st.session_state.students_data)}
            
            Key Insights:
            • Average attendance: {st.session_state.students_data['attendance'].mean():.1f}%
            • Scholarship eligibility rate: {(len(st.session_state.students_data[st.session_state.students_data['status'] == 'Scholarship Granted']) / len(st.session_state.students_data) * 100):.1f}%
            • Top performing subject: Mathematics (Average: {st.session_state.students_data['math'].mean():.1f})
            
            Detailed analysis and recommendations would be included in the full report.
            """
            
            st.download_button(
                label="📥 Download Full Report (PDF)",
                data=report_data,
                file_name=f"{report_type.replace(' ', '_')}_report.txt",
                mime="text/plain"
            )
    
    # Live Analytics Dashboard
    st.subheader("📊 Live Analytics Dashboard")
    
    # Performance Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        # Score Distribution
        fig_scores = px.histogram(
            st.session_state.students_data, 
            x='total_score', 
            title='Total Score Distribution',
            nbins=10,
            color_discrete_sequence=['#667eea']
        )
        fig_scores.add_vline(x=24, line_dash="dash", line_color="red", 
                            annotation_text="Scholarship Threshold (24)")
        st.plotly_chart(fig_scores, use_container_width=True)
    
    with col2:
        # Grade-wise Performance
        grade_performance = st.session_state.students_data.groupby('grade').agg({
            'attendance': 'mean',
            'academic_avg': 'mean',
            'total_score': 'mean'
        }).round(1)
        
        fig_grade = px.bar(
            grade_performance.reset_index(), 
            x='grade', 
            y=['attendance', 'academic_avg', 'total_score'],
            title='Grade-wise Performance Comparison',
            barmode='group'
        )
        st.plotly_chart(fig_grade, use_container_width=True)
    
    # Real-time Data Table
    st.subheader("🔴 Live Data View")
    
    # Add some interactive filters
    col1, col2 = st.columns(2)
    with col1:
        min_score = st.slider("Minimum Total Score", 0, 30, 0)
    with col2:
        show_columns = st.multiselect(
            "Select Columns to Display",
            ['name', 'grade', 'attendance', 'academic_avg', 'aptitude_score', 'total_score', 'status'],
            default=['name', 'grade', 'attendance', 'total_score', 'status']
        )
    
    filtered_table = st.session_state.students_data[
        st.session_state.students_data['total_score'] >= min_score
    ][show_columns]
    
    st.dataframe(
        filtered_table,
        use_container_width=True,
        hide_index=True
    )
    
    # Export functionality
    st.subheader("💾 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = st.session_state.students_data.to_csv(index=False)
        st.download_button(
            label="📄 Download as CSV",
            data=csv,
            file_name=f"pts_students_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        json_data = st.session_state.students_data.to_json(orient='records', indent=2)
        st.download_button(
            label="🔗 Download as JSON",
            data=json_data,
            file_name=f"pts_students_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col3:
        if st.button("🔄 Refresh Live Data"):
           st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>PTS Data Platform Demo | Built with Streamlit | Live Interactive Demo</p>
    <p>Add students, search data, generate reports - all in real-time!</p>
</div>
""", unsafe_allow_html=True)
