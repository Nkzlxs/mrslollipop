import requests
import re

class Covid19MY():

    def __init__(self):
        self.main()
        pass

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
        answer['article_src'] = first_hyperlink
        # print(first_hyperlink)

        """ Navigate to the fetched hyperlink """
        response = requests.get(url=first_hyperlink)
        res_text = response.text

        """ 
        Find the 3rd image, 
        1st one is currently kpk's logo,
        2nd one is discarded amount.
        """
        first_image_index = res_text.find("<img") #logo
        second_image_index = res_text.find("<img",first_image_index+1) #discard
        third_image_index = res_text.find("<img",second_image_index+1) #infographic
        src_pos = res_text.find("src=",third_image_index)

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
        temp = None
        output = ["cured","new","death"]

        # Cured Count -> new cases -> death count
        keywords1 = [
            "Jumlah kumulatif kes yang telah pulih sepenuhnya dari COVID-19",
            "jumlah kes positif COVID-19 di Malaysia",
            "jumlah kumulatif kes kematian COVID-19 di Malaysia"
            ]
        keywords2 = "kes"

        for n in range(0,len(keywords1)):
            # First filter
            re_unit = re.compile(
                pattern=f"{keywords1[n]}.*{keywords2}",
                flags=re.IGNORECASE
            )
            match_obj = re_unit.search(res_text)
            temp = match_obj[0]
            # print(match_obj[0])

            # Second filter
            re_unit = re.compile("(<[a-z]+>[ ]*\d+[ ]*([, ]+\d+){0,}[ ]*</[a-z]+>[ ]*.*kes)|(\d+[ ]*([, ]+\d+){0,}[ ]*kes)")
            match_obj = re_unit.search(temp)
            # print(match_obj[0])

            # Third filter
            re_unit = re.compile('\d')
            match_obj = re_unit.findall(match_obj[0])

            if match_obj:
                answer[output[n]] = int("".join(a for a in match_obj))
        print(answer)

        """ Return the fetched data and infographic url the the main program """
        return answer




if __name__ == "__main__":
    covid19my = Covid19MY()
