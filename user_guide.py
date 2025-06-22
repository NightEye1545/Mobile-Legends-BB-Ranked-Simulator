import streamlit as st

def user_guide():

    step_1 = """
    **Set Your Starting Rank**  
    Choose your current rank and number of stars.
    """

    step_2 = """
    **Set Your Target Rank**  
    Select where you want to reach (rank and stars).
    """

    step_3 = """
    **Adjust Simulation Settings** *(optional)*  
    - Change the number of simulated runs  
    - Set a maximum number of games to simulate  
    - Tweak win rate or trial chance if needed
    """

    step_4 = """
    **Click “Run Simulation”**  
    The system will simulate ranked matches to estimate how long it might take.
    """

    step_5 = """
    **Review the Graphs and Stats**  
    See estimated games required, histograms of outcomes, and other analysis.
    """

    tip = """
    💡 *Tip:* Try changing the win rate to see how performance affects your climb.
    """

    with st.expander("📘 How To Use The App", expanded=False):
        st.markdown(step_1)    
        with st.expander("1. Set Your Starting Rank"):
            st.write("test")
            
        st.markdown(step_2)
        with st.expander("2. Set Your Target Rank"):
            st.write("test")
            
        st.markdown(step_3)
        with st.expander("3. Adjust Simulation Settings (Optional)"):
             st.write("test")
            
        st.markdown(step_4)
        with st.expander("4. Run the Simulation"):
             st.write("test")
            
        st.markdown(step_5)
        with st.expander("5. Review the Graphs and Stats"):
             st.write("test")
            

        st.markdown("---")
        st.markdown(tip)

    with st.expander("📊 How To Interpret the Graphs", expanded=False):
            
            st.markdown("TEST      ")  