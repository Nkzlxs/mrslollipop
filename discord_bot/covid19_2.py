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
                """ Break on the first loop, because the first result will always be the first one """
                break

        """ Get the hyperlink encased within the quotes """
        first_hyperlink = res_text[first_quote+1:first_quote+dif]
        answer['article_src'] = first_hyperlink
        print(first_hyperlink)

        """ Navigate to the fetched hyperlink """
        response = requests.get(url=first_hyperlink)
        res_text = response.text

        """ 
        Find the case by states picture, src should contains "bm-kes-positif-negeri"
        """
        img_pattern = re.compile("<img.*src=\".*bm-kes-positif-negeri.*\"")
        match = img_pattern.search(res_text)

        
        if match is not None:
            link_pattern = re.compile("src=\".*bm-kes-positif-negeri.*\"")
            link = link_pattern.search(match[0])
            if link is not None:
                """ Find the first and last quote that contains the link to the latest infographic """
                first_quote = link[0].find("\"")
                end_quote = link[0].find("\"",first_quote+1)

                dif = end_quote - first_quote

                """ Here is the link to the infographic """
                src_link = link[0][first_quote+1:first_quote+dif]
                if src_link != "":
                    print(src_link)
                    answer['image_src'] = src_link
        else:
            answer['image_src'] = "https://i.stack.imgur.com/6M513.png"



        """ Find new cases, death count, cured count """
        temp = None
        output = ["cured","new","death"]

        # keywords1 = [
        #     "((Jumlah[ ]*(&nbsp;)*[ ]*kumulatif[ ]*(&nbsp;)*[ ]*kes[ ]*(&nbsp;)*[ ]*yang[ ]*(&nbsp;)*[ ]*telah[ ]*(&nbsp;)*[ ]*pulih[ ]*(&nbsp;)*[ ]*sepenuhnya[ ]*(&nbsp;)*[ ]*dari[ ]*(&nbsp;)*[ ]*COVID-19)|(Jumlah[ ]*(&nbsp;)*[ ]*kumulatif[ ]*(&nbsp;)*[ ]*kes[ ]*(&nbsp;)*[ ]*sembuh[ ]*(&nbsp;)*sepenuhnya[ ]*(&nbsp;)*[ ]*daripada[ ]*(&nbsp;)*[ ]*COVID-19))",
        #     "((jumlah[ ]*(&nbsp;)*[ ]*kes[ ]*(&nbsp;)*[ ]*positif[ ]*(&nbsp;)*[ ]*COVID-19[ ]*(&nbsp;)*[ ]*di[ ]*(&nbsp;)*[ ]*Malaysia)|(kes[ ]*(&nbsp;)*[ ]*positif[ ]*(&nbsp;)*[ ]*COVID-19[ ]*(&nbsp;)*[ ]*di[ ]*(&nbsp;)*[ ]*Malaysia))",
        #     "(jumlah[ ]*(&nbsp;)*[ ]*kumulatif[ ]*(&nbsp;)*[ ]*kes[ ]*(&nbsp;)*[ ]*kematian[ ]*(&nbsp;)*[ ]*COVID-19[ ]*(&nbsp;)*[ ]*di[ ]*(&nbsp;)*[ ]*Malaysia)"
        #     ]

        # Total Cured Count -> new cases -> death count
        keywords1 = [
            "Kes sembuh[ ]*(&nbsp;)*[ ]*",
            "Kes baharu[ ]*(&nbsp;)*[ ]*",
            "Kes kematian[ ]*(&nbsp;)*[ ]*"
        ]

        # keywords2 = "kes"
        keywords2 = "kumulatif"
        try:
            for n in range(0,len(keywords1)):

                print(n,end=" - ")
                
                # First filter
                re_unit = re.compile(
                    pattern="(%s.{0,50}%s)"%(keywords1[n],keywords2),
                    flags=re.IGNORECASE
                )
                match_obj = re_unit.search(res_text)
                temp = match_obj[0]
                print(match_obj[0])

                # Second filter, filtering html tags
                re_unit = re.compile("(<[a-z]+>[ ]*\([ ]*[\d+[ ]*([, ]+\d+){0,}[ ]*</[a-z]+>[ ]*.*kes[ ]*<)|(<[a-z]+>[ ]*\([ ]*\d+[ ]*([, ]+\d+){0,}[ ]*</[a-z]+>[ ]*.*kes)|(\([ ]*\d+[ ]*([, ]+\d+){0,}(&nbsp;)*[ ]*kes)")
                match_obj = re_unit.search(temp)
                print(match_obj[0])

                # Third filter
                re_unit = re.compile('\d')
                match_obj = re_unit.findall(match_obj[0])

                if match_obj:
                    answer[output[n]] = int("".join(a for a in match_obj))

            print(answer)
            """ Return the fetched data and infographic url the the main program """
            return answer

        except Exception as e:
            raise(e)





if __name__ == "__main__":
    covid19my = Covid19MY()
