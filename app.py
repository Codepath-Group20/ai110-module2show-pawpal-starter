import sys
from pathlib import Path
import streamlit as st

# --- PATH CONFIGURATION (AI-Native Safety) ---
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import your backend logic layers
from pawpal_system import Owner, Pet, Task, Scheduler


def render_schedule_briefing(schedule):
    """
    Render a short briefing below the Master Schedule table.
    - `schedule` is a chronological list of Task objects (earliest first).
    """
    if not schedule:
        st.info("No tasks in the master schedule to summarize.")
        return

    def is_high(p):
        if isinstance(p, str):
            return p.lower() in ("high", "critical")
        try:
            return int(p) >= 4
        except Exception:
            return False

    # High-priority warning + examples
    high_tasks = [t for t in schedule if is_high(getattr(t, "priority", None))]
    if high_tasks:
        st.markdown("⚠️ **Critical:** You have high-priority tasks scheduled.")
        for t in high_tasks[:3]:
            owner_name = next((p.name for p in st.session_state.owner.pets if t in p.tasks), "Unknown")
            st.markdown(f"- **{owner_name}**: {t.description} — {t.due_time}")

    # Next chronological task
    next_task = schedule[0]
    next_pet = next((p.name for p in st.session_state.owner.pets if next_task in p.tasks), "Unknown")
    st.markdown(f"**Next up:** {next_pet} — {next_task.description} at {next_task.due_time}")

    # Per-pet breakdown
    lines = []
    for pet in st.session_state.owner.pets:
        pet_tasks = [t for t in schedule if t in pet.tasks]
        if not pet_tasks:
            continue
        count = len(pet_tasks)
        earliest = next(t for t in schedule if t in pet_tasks)
        lines.append(f"- **{pet.name}**: {count} task{'s' if count != 1 else ''}; next at {earliest.due_time} — {earliest.description}")

    if lines:
        st.markdown("**Pet Breakdown:**")
        for ln in lines:
            st.markdown(ln)

# --- STREAMLIT PAGE LAYOUT ---
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.
This app serves as your interactive demo, fully integrated with your object-oriented backend.
"""
)

with st.expander("Scenario & Requirements", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. At minimum, your system should:
- Represent pet care tasks (what needs to happen, priority, due time)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
"""
    )

st.divider()

# --- 1. INITIALIZE PERSISTENT STATE ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- 2. PROFILE PROFILE SETUP (If no owner exists) ---
if st.session_state.owner is None:
    st.subheader("👤 Create Owner Profile")
    username = st.text_input("Enter your name to start your PawPal dashboard:")
    if username:
        st.session_state.owner = Owner(id="owner_01", name=username)
        st.rerun()

# --- 3. ACTIVE DASHBOARD (If owner exists) ---
else:
    st.subheader(f"🏠 {st.session_state.owner.name}'s Dashboard")
    
    # --- SECTION A: ADD A NEW PET ---
    with st.expander("➕ Register a New Pet", expanded=True):
        with st.form("add_pet_form", clear_on_submit=True):
            pet_name = st.text_input("Pet Name")
            species = st.selectbox("Species", ["dog", "cat", "bird", "other"])
            age = st.number_input("Age", min_value=0, max_value=30, value=1)
            submitted_pet = st.form_submit_button("Register Pet")

        if submitted_pet and pet_name:
            new_pet = Pet(
                id=f"pet_{len(st.session_state.owner.pets) + 1}",
                name=pet_name,
                species=species,
                age=int(age)
            )
            st.session_state.owner.add_pet(new_pet)
            st.success(f"🐾 {pet_name} has been successfully registered!")
            st.rerun()

    # --- SECTION B: MANAGE TASKS & SCHEDULING ---
    if not st.session_state.owner.pets:
        st.info("You haven't added any pets yet. Register a pet above to unlock scheduling features!")
    else:
        st.markdown("### 📋 Your Current Pets")
        for pet in st.session_state.owner.pets:
            st.write(f"- **{pet.name}** ({pet.species}, Age: {pet.age})")
            
        st.divider()
        
        # --- SECTION C: ADD A TASK TO A SPECIFIC PET ---
        st.subheader("📅 Add Pet Care Task")
        
        # Dropdown to select which pet gets the task
        pet_options = {pet.name: pet for pet in st.session_state.owner.pets}
        selected_pet_name = st.selectbox("Select target pet:", list(pet_options.keys()))
        target_pet = pet_options[selected_pet_name]
        
        with st.form("add_task_form", clear_on_submit=True):
            task_desc = st.text_input("Task Description (e.g., Morning Feeding)")
            priority_val = st.slider("Priority Level (1 = Low, 5 = High)", min_value=1, max_value=5, value=3)
            due_time_str = st.text_input("Due Time (e.g., 08:00, 04:30 PM, 2026-06-28 12:00)")
            task_freq = st.selectbox("Frequency", ["none", "daily", "weekly"])
            submitted_task = st.form_submit_button("Schedule Task")
            
        if submitted_task and task_desc and due_time_str:
            new_task = Task(
                id=f"task_{sum(len(p.tasks) for p in st.session_state.owner.pets) + 1}",
                description=task_desc,
                priority=priority_val,
                due_time=due_time_str,
                is_completed=False
            )
            # Assign the frequency attribute added in Phase 4
            if hasattr(new_task, 'frequency'):
                new_task.frequency = task_freq
                
            # Add directly using your OOP method
            target_pet.add_task(new_task)
            st.success(f"Added task for {target_pet.name}: '{task_desc}' due at {due_time_str} (Frequency: {task_freq})")
            st.rerun()

        st.divider()

        # --- SECTION D: GENERATE DAILY CHRONOLOGICAL AGENDA ---
        st.subheader("⏳ Generate Chronological Schedule")
        st.caption("This initializes your Scheduler class and sorts all tasks from your pets.")
        
        # Phase 4 Interactive Filtering UI
        st.markdown("#### 🔍 Filter Options")
        col1, col2 = st.columns(2)
        with col1:
            filter_pet = st.selectbox("Filter by Pet", ["All"] + list(pet_options.keys()))
        with col2:
            filter_status = st.selectbox("Filter by Status", ["All Incomplete", "All Completed", "Show Everything"])

        if st.button("Generate Master Schedule"):
            # Instantiate the scheduler using our dynamic memory data
            scheduler = Scheduler(owner=st.session_state.owner)

            st.markdown("### ⚠️ Schedule Health Warnings")
            conflicts = scheduler.detect_conflicts()
            if conflicts:
                st.warning("Potential scheduling conflicts detected:")
                for warning in conflicts:
                    st.warning(warning)
            else:
                st.success("✅ No scheduling conflicts detected!")

            # Build the master schedule in strict chronological order first.
            master_schedule = scheduler.build_schedule()

            # Apply the Phase 4 filter logic while preserving the chronological order.
            pet_filter_arg = None if filter_pet == "All" else filter_pet
            status_filter_arg = None
            if filter_status == "All Incomplete":
                status_filter_arg = False
            elif filter_status == "All Completed":
                status_filter_arg = True

            if pet_filter_arg is not None or status_filter_arg is not None:
                master_schedule = [
                    task
                    for task in master_schedule
                    if (pet_filter_arg is None or any(
                        pet.name == pet_filter_arg for pet in st.session_state.owner.pets if task in pet.tasks
                    ))
                    and (status_filter_arg is None or task.is_completed is status_filter_arg)
                ]

            if not master_schedule:
                st.info("No tasks left on the agenda matching your filter constraints.")
            else:
                st.success("Chronological Schedule Processed Successfully!")
                st.caption("Tasks are displayed in strict chronological order using the scheduler's built-in ordering.")

                # Render out the results into a clean list structure.
                schedule_data = []
                for task in master_schedule:
                    owning_pet = next((p.name for p in st.session_state.owner.pets if task in p.tasks), "Unknown")
                    schedule_data.append({
                        "Pet": owning_pet,
                        "Time Due": task.due_time,
                        "Task Description": task.description,
                        "Priority": task.priority,
                        "Frequency": getattr(task, 'frequency', 'none'),
                        "Status": "✅ Done" if task.is_completed else "⏳ Pending"
                    })

                st.markdown("### 📋 Master Schedule Rows")
                for row in schedule_data:
                    time_str = row.get("Time Due", "N/A")
                    pet_str = row.get("Pet", "N/A")
                    task_str = row.get("Task Description", "N/A")
                    priority_str = row.get("Priority", "N/A")
                    freq_str = row.get("Frequency", "none")
                    status_str = row.get("Status", "⏳ Pending")

                    recur_icon = " 🔄" if freq_str != "none" else ""

                    st.markdown(f"⏱️ **{time_str}**{recur_icon} | 🐾 **{pet_str}** | 📝 {task_str} | 🔴 *Priority: {priority_str}* | {status_str}")

                st.write("---")
                render_schedule_briefing(master_schedule)
