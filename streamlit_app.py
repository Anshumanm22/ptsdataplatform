# streamlit_app.py
# Fixed version with proper column names and role-based access

import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Page config
st.set_page_config(
    page_title="PTS Data Platform",
    page_icon="🎓",
    layout="wide"
)

# Define users BEFORE the function
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

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
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

# Initialize session state with new data structure
if 'students_data' not in st.session_state:
    st.session_state.students_data = pd.DataFrame({
        'name': ['Ananya Chakraborty', 'Rahul Mondal', 'Priya Das', 'Amit Kumar', 'Sneha Roy'],
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
    
    # Calculate average attendance
    st.session_state.students_data['attendance_avg'] = (
        st.session_state.students_data['attendance_mid'] + 
        st.session_state.students_data['attendance_end']
    ) / 2
    
    # Calculate academic averages
    st.session_state.students_data['mid_year_avg'] = (
        st.session_state.students_data['mid_year_math'] +
        st.session_state.students_data['mid_year_english'] +
        st.session_state.students_data['mid_year_science']
    ) / 3
    
    st.session_state.students_data['end_year_avg'] = (
        st.session_state.students_data['end_year_math'] +
        st.session_state.students_data['end_year_english'] +
        st.session_state.students_data['end_year_science']
    ) / 3

if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# Header
st.markdown("""
<div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🎓 Peerless Trinity Scholarship</h1>
    <p style='color: white; margin: 0; font-size: 1.2rem; opacity: 0.9;'>Data Management Platform - Live Demo</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with logout
with st.sidebar:
    st.write(f"Logged in as: **{st.session_state['user_name']}**")
    st.write(f"Role: {st.session_state['role'].title()}")
    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.sidebar.header("Platform Navigation")

# Role-based page options
if st.session_state["role"] == "admin":
    page_options = ["Dashboard Overview", "Student Details", "Scholarship Approvals", "Reports & Analytics"]
elif st.session_state["role"] == "teacher":
    page_options = ["Dashboard Overview", "Student Details", "Data Entry"]
else:  # coordinator
    page_options = ["Dashboard Overview", "Reports & Analytics"]

page = st.sidebar.selectbox("Select Page", page_options)

# Success message
if st.session_state.show_success:
    st.success("✅ Data saved successfully!")
    st.session_state.show_success = False

# Dashboard Overview Page - Role-based
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
            display_data = center_students[['name', 'grade', 'attendance_avg', 'entry_score', 'scholarship_status']].copy()
            display_data.columns = ['Name', 'Grade', 'Attendance %', 'Entry Score', 'Status']
            st.dataframe(display_data, use_container_width=True, hide_index=True)
    
    elif st.session_state["role"] == "teacher":
        st.header("👩‍🏫 Teacher Dashboard - My Students")
        
        # Filter students assigned to this teacher
        teacher_students = st.session_state.students_data[
            st.session_state.students_data['teacher_assigned'] == 'Teacher A'
        ]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("My Students", len(teacher_students), delta="Assigned")
        with col2:
            st.metric("Avg Attendance", f"{teacher_students['attendance_avg'].mean():.1f}%", delta="My Class")
        with col3:
            active_count = len(teacher_students[teacher_students['scholarship_status'] == 'Active'])
            st.metric("Active Scholarships", active_count, delta="Current")
        
        st.subheader("📚 My Assigned Students")
        
        # Detailed student cards for teacher
        for idx, student in teacher_students.iterrows():
            with st.expander(f"👤 {student['name']} - Grade {student['grade']}", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**Attendance:** {student['attendance_avg']:.1f}%")
                with col2:
                    st.write(f"**Mid-Year Avg:** {student['mid_year_avg']:.1f}%")
                with col3:
                    st.write(f"**End-Year Avg:** {student['end_year_avg']:.1f}%")
                with col4:
                    st.write(f"**Status:** {student['scholarship_status']}")
                
                # Subject breakdown
                subjects = ['Math', 'English', 'Science']
                mid_scores = [student['mid_year_math'], student['mid_year_english'], student['mid_year_science']]
                end_scores = [student['end_year_math'], student['end_year_english'], student['end_year_science']]
                
                subject_df = pd.DataFrame({
                    'Subject': subjects,
                    'Mid-Year': mid_scores,
                    'End-Year': end_scores
                })
                st.bar_chart(subject_df.set_index('Subject'))
    
    elif st.session_state["role"] == "coordinator":
        st.header("🏛️ Coordinator Dashboard - Center Management")
        
        # Center-specific data
        my_center = "Saltlake Center"
        center_students = st.session_state.students_data[st.session_state.students_data['center'] == my_center]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Center Students", len(center_students), delta=my_center)
        with col2:
            st.metric("Avg Attendance", f"{center_students['attendance_avg'].mean():.1f}%", delta="Center Average")
        with col3:
            active_count = len(center_students[center_students['scholarship_status'] == 'Active'])
            st.metric("Active Scholarships", active_count, delta="This Center")
        with col4:
            at_risk = len(center_students[center_students['attendance_avg'] < 90])
            st.metric("At-Risk Students", at_risk, delta="Need Support")
        
        # Grade-wise breakdown
        st.subheader("📊 Grade-wise Performance")
        grade_stats = center_students.groupby('grade').agg({
            'attendance_avg': 'mean',
            'entry_score': 'mean',
            'name': 'count'
        }).round(1)
        grade_stats.columns = ['Avg Attendance', 'Avg Entry Score', 'Student Count']
        st.dataframe(grade_stats, use_container_width=True)
        
        # Student overview table
        st.subheader("👥 All Center Students")
        display_data = center_students[['name', 'grade', 'attendance_avg', 'entry_score', 'scholarship_status']].copy()
        display_data.columns = ['Name', 'Grade', 'Attendance %', 'Entry Score', 'Status']
        st.dataframe(display_data, use_container_width=True, hide_index=True)
        
        # Action items
        st.subheader("⚠️ Attention Required")
        at_risk = center_students[center_students['attendance_avg'] < 90]
        if len(at_risk) > 0:
            st.warning(f"{len(at_risk)} students have attendance below 90%")
            st.dataframe(at_risk[['name', 'grade', 'attendance_avg']], hide_index=True)
        else:
            st.success("All students maintaining good attendance!")

# Student Details Page
elif page == "Student Details":
    st.header("👤 Individual Student Analysis")
    
    if 'selected_student' not in st.session_state:
        st.info("Select a student to view detailed analysis")
        
        # Student selector
        student_names = st.session_state.students_data['name'].tolist()
        selected_name = st.selectbox("Select a student:", ["Choose a student..."] + student_names)
        
        if selected_name != "Choose a student...":
            selected_row = st.session_state.students_data[st.session_state.students_data['name'] == selected_name].iloc[0]
            st.session_state.selected_student = selected_row.to_dict()
    
    if 'selected_student' in st.session_state:
        student = st.session_state.selected_student
        
        # Student Header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"## {student['name']}")
            st.caption(f"Grade {student['grade']} • {student['center']}")
        
        with col2:
            if st.button("← Back"):
                del st.session_state.selected_student
                st.rerun()
        
        # Performance Summary
        st.subheader("📊 Performance Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Entry Score", f"{student['entry_score']}/30")
        with col2:
            st.metric("Avg Attendance", f"{student['attendance_avg']:.1f}%")
        with col3:
            st.metric("Mid-Year Avg", f"{student['mid_year_avg']:.1f}%")
        with col4:
            st.metric("End-Year Avg", f"{student['end_year_avg']:.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Subject Performance - Mid-Year**")
            subjects = ['Math', 'English', 'Science']
            scores = [student['mid_year_math'], student['mid_year_english'], student['mid_year_science']]
            subject_df = pd.DataFrame({'Subject': subjects, 'Score': scores})
            st.bar_chart(subject_df.set_index('Subject'))
        
        with col2:
            st.write("**Subject Performance - End-Year**")
            scores_end = [student['end_year_math'], student['end_year_english'], student['end_year_science']]
            subject_df_end = pd.DataFrame({'Subject': subjects, 'Score': scores_end})
            st.bar_chart(subject_df_end.set_index('Subject'))

# Data Entry Page - Teachers Only
elif page == "Data Entry":
    if st.session_state["role"] != "teacher":
        st.error("Access Denied: Only teachers can enter assessment data")
        st.stop()
    
    st.header("📝 Teacher Data Entry - Assessment Scores")
    
    # Filter students assigned to this teacher
    assigned_students = st.session_state.students_data[
        st.session_state.students_data['teacher_assigned'] == 'Teacher A'
    ]
    
    with st.form("assessment_entry"):
        student_name = st.selectbox("Select Student", assigned_students['name'].tolist())
        assessment_period = st.selectbox("Assessment Period", ["Mid-Year", "End-Year"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            math_score = st.number_input("Mathematics Score", 0, 100, 75)
        with col2:
            english_score = st.number_input("English Score", 0, 100, 75)
        with col3:
            science_score = st.number_input("Science Score", 0, 100, 75)
        
        attendance = st.slider("Attendance %", 0, 100, 90)
        
        if st.form_submit_button("💾 Save Assessment Data", type="primary"):
            # Update the dataframe
            student_idx = st.session_state.students_data[
                st.session_state.students_data['name'] == student_name
            ].index[0]
            
            if assessment_period == "Mid-Year":
                st.session_state.students_data.loc[student_idx, 'mid_year_math'] = math_score
                st.session_state.students_data.loc[student_idx, 'mid_year_english'] = english_score
                st.session_state.students_data.loc[student_idx, 'mid_year_science'] = science_score
                st.session_state.students_data.loc[student_idx, 'attendance_mid'] = attendance
                
                # Recalculate mid-year average
                st.session_state.students_data.loc[student_idx, 'mid_year_avg'] = (
                    math_score + english_score + science_score
                ) / 3
            else:
                st.session_state.students_data.loc[student_idx, 'end_year_math'] = math_score
                st.session_state.students_data.loc[student_idx, 'end_year_english'] = english_score
                st.session_state.students_data.loc[student_idx, 'end_year_science'] = science_score
                st.session_state.students_data.loc[student_idx, 'attendance_end'] = attendance
                
                # Recalculate end-year average
                st.session_state.students_data.loc[student_idx, 'end_year_avg'] = (
                    math_score + english_score + science_score
                ) / 3
            
            # Recalculate average attendance
            st.session_state.students_data.loc[student_idx, 'attendance_avg'] = (
                st.session_state.students_data.loc[student_idx, 'attendance_mid'] +
                st.session_state.students_data.loc[student_idx, 'attendance_end']
            ) / 2
            
            st.session_state.show_success = True
            st.rerun()

# Scholarship Approvals - Admin Only
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
        st.success("✅ No pending approval requests")
        
        # Show approved/rejected students
        st.subheader("Previously Processed")
        processed = st.session_state.students_data[
            (st.session_state.students_data['grade'] == 9) & 
            (~st.session_state.students_data['continuation_approved'].isna())
        ]
        if len(processed) > 0:
            st.dataframe(processed[['name', 'end_year_avg', 'attendance_end', 'continuation_approved']], hide_index=True)
    else:
        st.subheader("📋 Pending Approvals for Grade 9 → Grade 10 Continuation")
        
        for idx, student in grade_9_students.iterrows():
            with st.expander(f"Review: {student['name']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Performance Summary**")
                    st.write(f"Entry Score: {student['entry_score']}/30")
                    st.write(f"Mid-Year Avg: {student['mid_year_avg']:.1f}%")
                    st.write(f"End-Year Avg: {student['end_year_avg']:.1f}%")
                
                with col2:
                    st.write("**Attendance**")
                    st.write(f"Mid-Year: {student['attendance_mid']}%")
                    st.write(f"End-Year: {student['attendance_end']}%")
                    st.write(f"Average: {student['attendance_avg']:.1f}%")
                    
                with col3:
                    st.write("**Recommendation**")
                    end_avg = student['end_year_avg']
                    if end_avg >= 75 and student['attendance_end'] >= 90:
                        st.success("✅ Recommended for Continuation")
                    elif end_avg >= 70 and student['attendance_end'] >= 85:
                        st.warning("⚠️ Conditional Continuation")
                    else:
                        st.error("❌ At Risk - Review Required")
                
                # Approval buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"✅ Approve", key=f"approve_{idx}"):
                        st.session_state.students_data.loc[idx, 'continuation_approved'] = 'Approved'
                        st.session_state.students_data.loc[idx, 'scholarship_status'] = 'Active'
                        st.success(f"Approved continuation for {student['name']}")
                        st.rerun()
                
                with col2:
                    if st.button(f"❌ Reject", key=f"reject_{idx}"):
                        st.session_state.students_data.loc[idx, 'continuation_approved'] = 'Rejected'
                        st.session_state.students_data.loc[idx, 'scholarship_status'] = 'Discontinued'
                        st.error(f"Rejected continuation for {student['name']}")
                        st.rerun()
                
                with col3:
                    if st.button(f"⏸️ Hold", key=f"hold_{idx}"):
                        st.session_state.students_data.loc[idx, 'continuation_approved'] = 'On Hold'
                        st.session_state.students_data.loc[idx, 'scholarship_status'] = 'Under Review'
                        st.warning(f"Put {student['name']} on hold")
                        st.rerun()

# Reports & Analytics
elif page == "Reports & Analytics":
    st.header("📈 Reports & Analytics")
    
    # Generate Report Section
    st.subheader("📄 Generate Custom Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox("Report Type", [
            "Student Performance Summary",
            "Attendance Analysis",
            "Scholarship Status Report",
            "Grade 9 Continuation Report"
        ])
    
    with col2:
        grade_filter = st.selectbox("Grade Filter", ["All Grades", "Grade 9", "Grade 10"])
    
    if st.button("🚀 Generate Report", type="primary"):
        with st.spinner("Generating report..."):
            import time
            time.sleep(2)
            
            filtered_data = st.session_state.students_data.copy()
            if grade_filter != "All Grades":
                grade_num = 9 if grade_filter == "Grade 9" else 10
                filtered_data = filtered_data[filtered_data['grade'] == grade_num]
            
            st.success("✅ Report generated successfully!")
            
            # Display summary
            st.subheader(f"{report_type} - Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Students", len(filtered_data))
            with col2:
                st.metric("Avg Attendance", f"{filtered_data['attendance_avg'].mean():.1f}%")
            with col3:
                active = len(filtered_data[filtered_data['scholarship_status'] == 'Active'])
                st.metric("Active Scholarships", active)
            
            # Detailed data table
            st.subheader("Detailed Data")
            st.dataframe(filtered_data[['name', 'grade', 'attendance_avg', 'mid_year_avg', 'end_year_avg', 'scholarship_status']], 
                        use_container_width=True, hide_index=True)
    
    # Analytics Dashboard
    st.subheader("📊 Live Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Attendance Distribution**")
        st.bar_chart(st.session_state.students_data.set_index('name')['attendance_avg'])
    
    with col2:
        st.write("**Scholarship Status**")
        status_counts = st.session_state.students_data['scholarship_status'].value_counts()
        st.bar_chart(status_counts)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>PTS Data Platform | Built with Streamlit | Role-Based Access Control</p>
</div>
""", unsafe_allow_html=True)
