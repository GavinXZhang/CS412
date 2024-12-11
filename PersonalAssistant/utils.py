import calendar
from datetime import date

def get_month_calendar(year, month, events):
    cal = calendar.Calendar()
    month_days = cal.itermonthdays2(year, month)  # Generates day numbers and weekday pairs
    today = date.today()

    # Create a dictionary of days and events
    calendar_data = []
    for day, weekday in month_days:
        day_data = {
            'day': day,
            'weekday': weekday,
            'events': [],
        }
        if day > 0:  # Valid days only
            day_date = date(year, month, day)
            day_events = [event for event in events if event.start_time.date() <= day_date <= event.end_time.date()]
            day_data['events'] = day_events
            day_data['is_today'] = day_date == today
        calendar_data.append(day_data)

    return calendar_data
import openai
import os
import asyncio
# Set your OpenAI API key

def generate_summary(user, events, reminders, missed_calls):
    # Prepare data for summary
    events_summary = "\n".join([f"- {event.title} on {event.start_time}" for event in events])
    reminders_summary = "\n".join([f"- {reminder.message} at {reminder.reminder_time}" for reminder in reminders])
    missed_calls_summary = "\n".join([f"- Call from {call.contact_name} at {call.call_time}" for call in missed_calls])

    # Create the summary prompt
    return f"""
    Hi {user.username}, here's your summary:

    **Upcoming Events:**
    {events_summary}

    **Reminders:**
    {reminders_summary}

    **Missed Calls:**
    {missed_calls_summary}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        if "quota" in str(e).lower():
            return "Your assistant is unavailable due to quota limits. Please try again later."
        else:
            return f"Unexpected error: {e}"