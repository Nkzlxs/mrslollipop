import requests

class Covid19MY():

    def __init__(self):
        self.main()

    def main(self):
        answer = {}

        """ Navigate to main page """
        response = requests.get(url="https://kpkesihatan.com/")
        # response = requests.get(url="https://www.facebook.com")
        res_text = response.text

        """ Find the div with id main-content """
        maincontent_index = res_text.find("<div id=\"main-content\">")

        """ Find the hyperlinks, which are also the first element in each article """
        a_link = res_text.find("<a href=",maincontent_index)
        zeroth_link = res_text.find("<a href=",maincontent_index) # let the program remember the first <a href= position

        while True:
            """ Find the first and last quote that contains the link to the latest case """
            first_quote = res_text.find("\"",a_link)
            end_quote = res_text.find("\"",first_quote+1)

            dif = end_quote - first_quote
            # print(f"String length: {dif}")

            """ Verify if it is about the latest covid19 information or not """
            keywords = "situasi-semasa-jangkitan-penyakit-coronavirus-2019-covid-19-di-malaysia"
            verify_word = res_text.find(keywords,first_quote,end_quote)
            if verify_word == -1:
                """ If there's no keywords in the first hyperlink, skip to the next one """
                a_link = res_text.find("<a href=",a_link+len("<a href="))

                """ When the search for "<a href=" returned to the beginning """
                if a_link == zeroth_link:
                    exit("No specifed keywords found! Exiting...") # terminate the program
            else:
                break
                pass
                # print("Keyword found!")

        """ Get the hyperlink encased within the quotes """
        first_hyperlink = res_text[first_quote+1:first_quote+dif]
        # print(first_hyperlink)

        """ Navigate to the fetched hyperlink """
        response = requests.get(url=first_hyperlink)
        res_text = response.text

        """ Find the 2nd image, 1st one is currently kpk's logo """
        first_image_index = res_text.find("<img") #logo
        second_image_index = res_text.find("<img",first_image_index+1) #poster
        src_pos = res_text.find("src=",second_image_index)

        """ Find the first and last quote that contains the link to the latest infographic """
        first_quote = res_text.find("\"",src_pos)
        end_quote = res_text.find("\"",first_quote+1)

        dif = end_quote - first_quote
        # print(f"String length: {dif}")

        """ Here is the link to the infographic """
        src_link = res_text[first_quote+1:first_quote+dif]
        # print(src_link)
        answer['image_src'] = src_link


        """ Find new cases, death count, cured count """
        digits = []
        temp = None
        output = ["cured","new","death"]

        # Cured Count > new cases > death count
        keywords1 = [
            "Jumlah kumulatif kes yang telah pulih sepenuhnya dari COVID-19",
            "jumlah kes positif COVID-19 di Malaysia",
            "jumlah kumulatif kes kematian COVID-19 di Malaysia"
            ]
        keywords2 = "sebanyak"
        keywords3 = "kes"

        for n in range(0,len(keywords1)):
            digits = []
            num1 = res_text.find(keywords1[n])
            num2 = res_text.find(keywords2,num1)
            num3 = res_text.find(keywords3,num2)

            temp = res_text[num2+len(keywords2):num3]
            for x in temp:
                if x.isdigit():
                    digits.append(x)

            a_string = ""
            for x in digits:
                a_string += x
            # print(f"{output[n]}: {int(a_string)}")
            answer[output[n]] = int(a_string)

        print(answer)

        """ Return the fetched data and infographic url the the main program """
        return answer




if __name__ == "__main__":
    covid19my = Covid19MY()
