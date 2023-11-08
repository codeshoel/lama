import os
import datetime
from email.message import EmailMessage
import logging
from dotenv import dotenv_values


# class Backup:

    # """
    #     The backup Object incopass methods that handle the removal of backed up data
    #     on the server to free up memory space for further backup.
    # """

def remove_backup(dir, days):
        # Get current time
    current_time = datetime.datetime.now()
    try:
        # Calculate cutoff date based on the number of days
        cutoff_date = current_time - datetime.timedelta(days=days)
        even_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_loop =  {}
        # Loop through the files in the directory
        for root, dirs, files in os.walk(dir):
            if len(files) > 0:
                file_loop['name'] = []
                file_loop['status'] = []
                file_loop['date'] = []
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

                        # Check if the file's modification time is older than the cutoff date
                        if file_modified_time >= cutoff_date:
                            # print(f"Deleting {file_path} - Last Modified: {file_modified_time}")

                            try:
                            # Remove file(s)
                                os.remove(file_path)
                                file_loop['name'].append(file)
                                file_loop['status'].append("[Pass]")
                                file_loop['date'].append(even_date)
                                print("Task completed with no exception...!")

                            except OSError as e:
                                file_loop['name'].append(file)
                                file_loop['status'].append("[Failed]")
                                file_loop['date'].append(even_date)
                                print("Task completed with exception...!")
                                return log_error(e)
                        else:
                            res = f"No file affected(All file are lower than /OR equel to specified date/time) {cutoff_date}."
                            return log_error(res)
                    except Exception  as e:
                        return log_error(e)

                # Call audit function to send audit email
                if iter(file_loop):
                    return audit(file_loop)
                else:
                    pass

            else:
                res = 'Specified directory is empty.'
                return log_error(res)


    except Exception as e:
        return log_error(e)

def retain():
    # This function handles the transmitting of data to another server for retainship.
    pass

def audit(reports):
    import smtplib

    try:

        # template setup
        email_html_template = "<div style='padding: 10px; width: 600px; display: flexmportant; flex-direction: column; justify-content: center !important !important !i;'>"
        email_html_template+=f"<p>Hello, Lama here!, Find below list of backup files removed to free memory space for future backup.</p><br/>"
        for index in range(0, len(reports['name'])):

        # if index < len(reports['name']):
            task = 'Task ['+ str(index+1)+']: '
            name = reports['name'][index]
            status = reports['status'][index]
            date = reports['date'][index]

            email_html_template += f"""
                <div style='color: #616161; width: 500px; display: block !important; padding: 15px; border-radius: 3px; box-shadow: 2px 2px 4px 2px #999 !important;'>
                    <div style='display: flex !important; flex-direction: row !important; justify-content: space-between !important;'>
                        <div>{name}</div>
                        <div style='color: #00A100; font-weight: bold;'>{status}</div>
                    </div>
                    <hr/>
                    <div style='display: flex !important; flex-direction: row !important; justify-content: center !important;'>
                        <i>{date}</i>
                    </div>
                </div>
            """
            email_html_template +="<br/>"
        email_html_template+="</div>"

        # initialize env
        env = dotenv_values('.env')
        
        # Access env variables
        if env:
            email_addr = env.get('EMAIL_ADDR')
            password = env.get('PASSWORD')
            port = env.get('PORT')
            host = env.get('HOST')
            
            # Email content
            email = EmailMessage()
            email['From'] = email_addr
            email['To'] = email_addr
            email['Subject'] = 'CRM Backup Server Cleanup Report(From Lama)'

            # Add HTML content to the email
            email.add_alternative(email_html_template, subtype='html')

            # Establish connection to SMTP server
            with smtplib.SMTP_SSL(host=host, port=port) as server:
                server.set_debuglevel(1)
                # server.starttls()  # Enable TLS encryption
                server.ehlo()
                server.login(email_addr, password)  # Use app password if 2-step verification is enabled
                print("processing..")
                server.send_message(email)
                print("Message sent..!")
                server.quit()
        else:
            print("No variable found in .env file")

    except Exception as e:
        return log_error(e)


def log_error(error):
    try:
        logging.basicConfig(
        filename='error.log', 
        level=logging.ERROR, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        return logging.error(f"log[EXCEPTION]: {error}", exc_info=True)
         
    except Exception as e:
        return e

if __name__ == '__main__':
    daily = int(1)
    days_in_week = int(7)
    days_in_month = int(30)
    days_in_year = int(365)
    dir='G:/back_it/66'

    # run = Backup()
    remove_backup(dir, days_in_week)




