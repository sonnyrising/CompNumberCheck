import pandas as pd
import bisect

class Criteria_Class:
    def __init__(self, country, compNum):
        self.country = country
        self.compNum = compNum

    def getCountry(self):
        return self.country
    def getCompNum(self):
        return self.compNum

    def setCountry(self, country):
        self.country = country
    def setCompNum(self, compNum):
        self.compNum = compNum


class Checker:
    def __init__(self):
        self.df = pd.read_csv("OGN.csv")

    ##Check if the comp number exists in that country
    def check_for_cn(self, criteria):
        filtered_df = self.df[self.df["COUNTRY"] == criteria.getCountry()]

        target_cn = criteria.getCompNum()

        # 3. Perform the search on the filtered local dataframe
        idx = filtered_df["CN"].searchsorted(target_cn)

        if idx < len(filtered_df) and filtered_df["CN"].iloc[idx] == target_cn:
            return True
        return False

    def UI(self, cn, country):
        criteria = Criteria_Class(country, cn)
        return self.check_for_cn(criteria)


cn = input("Enter the comp number: ")
country = input("Enter the country: ")
print(Checker().UI(cn, country))


