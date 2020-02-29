


class Bbox:
    """
    This is a class to structure the bounding box data
    Attributes:
        Name (string): Name of the interface
        minX (int) : minimum value in the x direction
        maxX (int) : maximum value in the x direction
        minY (int) : minimum value in the y direction
        maxY (int) : maximum value in the y direction
    """
    def __init__(self, name, minX, minY, maxX, maxY):
        """
        This is the constructor of the class
        Parameter:
            Name (string): Name of the interface
            minX (int) : minimum value in the x direction
            maxX (int) : maximum value in the x direction
            minY (int) : minimum value in the y direction
            maxY (int) : maximum value in the y direction
        """
        self.name = name
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY


class InterfaceBbox:
    """
    This is a class acts as wrapper around the Bbox data structure
     and interface with the outside applications
    Attributes:
        intfName (string): Name of the interface
    """
    def __init__(self, intfName):
        """
        This is the constructor to the class
        Parameters:
            intfName (string): Name of the interface
        """
        self.bboxList = []
        self.Name = intfName

    def addBbox(self, bboxInstance):
        """
        This stores the new Bbox instance on to a list
        Parameters:
            bboxInstance (Bbox): Instance of the Bbox class
        """
        self.bboxList.append(bboxInstance)

    def whichBbox(self, x, y):
        """
        This indicates if the location co-ordinates (x,y) lies inside our outside the Bbox
        Parameters:
            x (int): location on x axis
            y (int): location on y axis

        Returns:
            boolean: true is (x,y) lies inside Bbox, false otherwise
        """
        for bboxIns in self.bboxList:
            if bboxIns.minX < x < bboxIns.maxX:
                if bboxIns.minY < y < bboxIns.maxY:
                    return bboxIns.name
        return "None"


class PosData:
    """
    This is a class to manages and controls the data read at the
    mentioned data points for the users and provides methods
    to analyse the information better
    Attributes:
        normTime (float): normalized time
        normTime (float): corresponding actual time
        mouse (tuple): Mouse Position
        cursor (tuple): Cursor Position
        fixation (tuple): Fixation Position
        interfaceObj (InterfaceBbox): Bounding box data for the interface

    """
    def __init__(self, normTime, actualTime, mouse, cursor, fixation, interfaceObj):
        """
        This is a constructor to the class

        Parameters:
            normTime (float): normalized time
            normTime (float): corresponding actual time
            mouse (tuple): Mouse Position
            cursor (tuple): Cursor Position
            fixation (tuple): Fixation Position
            interfaceObj (InterfaceBbox): Bounding box data for the interface

        """
        self.timestamp = normTime
        self.mouse_data = mouse
        self.fixation_data = fixation
        self.actualTimestamp = actualTime
        self.cursor_data = cursor
        self.valBbox = interfaceObj.whichBbox(self.mouse_data[0][0], self.mouse_data[0][1])

    def describe(self):
        """
        This method prints the summary of the data contained in it

        """
        print(self.timestamp, end=" ")
        print(self.actualTimestamp, end=" ")
        print(self.mouse_data, end=" ")
        print(self.cursor_data, end=" ")
        print(self.fixation_data, end=" ")
        print(self.valBbox)

class BoundingBox:
    """
    This class contains all the InterfaceBbox instances for the given provided dataset.
    """
    @staticmethod
    def getBoundingBoxInfo():

        """
        This is a static method of the class which return a dictionary containing
         all the InterfaceBbox instances

        Returns:
            dictOfInterfaceBbox: dictionary - [Interface name : InterfaceBbox objects ]

        """

        dictOfInterfaceBbox = {}

        oBlogger_5_Bbox = InterfaceBbox("Blogger_5")
        oBlogger_5_Bbox.addBbox(Bbox("1_Title", 625, 164, 1319, 212))
        oBlogger_5_Bbox.addBbox(Bbox("1_Text", 626, 234, 1322, 838))
        oBlogger_5_Bbox.addBbox(Bbox("1_LeftButton1", 557, 237, 621, 274))
        oBlogger_5_Bbox.addBbox(Bbox("1_LeftButton2", 566, 277, 617, 305))
        oBlogger_5_Bbox.addBbox(Bbox("1_LeftButton3", 584, 308, 620, 428))
        oBlogger_5_Bbox.addBbox(Bbox("1_LeftButton4", 583, 433, 621, 560))
        oBlogger_5_Bbox.addBbox(Bbox("1_RightButton1", 1344, 164, 1465, 281))
        oBlogger_5_Bbox.addBbox(Bbox("1_RightButton2", 1353, 323, 1500, 409))
        oBlogger_5_Bbox.addBbox(Bbox("1_RightButton3", 1356, 443, 1510, 531))
        dictOfInterfaceBbox["Blogger_5"] = oBlogger_5_Bbox

        oGmailBbox = InterfaceBbox("gmail")
        oGmailBbox.addBbox(Bbox("2_Title", 629, 165, 1320, 210))
        oGmailBbox.addBbox(Bbox("2_UnderTitle", 626, 214, 1318, 257))
        oGmailBbox.addBbox(Bbox("2_Text", 628, 270, 1316, 860))
        oGmailBbox.addBbox(Bbox("2_ButtonLeft", 628, 866, 862, 900))
        oGmailBbox.addBbox(Bbox("2_ButtonRight", 865, 865, 1120, 899))
        oGmailBbox.addBbox(Bbox("2_Delete", 1277, 865, 1325, 898))
        dictOfInterfaceBbox["gmail"] = oGmailBbox

        oBlogger_2_Bbox = InterfaceBbox("Blogger_2")
        oBlogger_2_Bbox.addBbox(Bbox("3_Title", 625, 164, 1319, 212))
        oBlogger_2_Bbox.addBbox(Bbox("3_Text", 626, 234, 1322, 838))
        oBlogger_2_Bbox.addBbox(Bbox("3_Buttons", 628, 835, 991, 871))
        oBlogger_2_Bbox.addBbox(Bbox("3_Photo", 626, 874, 709, 985))
        oBlogger_2_Bbox.addBbox(Bbox("3_Comments", 725, 876, 894, 980))
        oBlogger_2_Bbox.addBbox(Bbox("3_Privacy", 908, 880, 1039, 978))
        oBlogger_2_Bbox.addBbox(Bbox("3_Delete", 1277, 865, 1325, 898))
        dictOfInterfaceBbox["Blogger_2"] = oBlogger_2_Bbox

        oFB_photo_Bbox = InterfaceBbox("FB_photo")
        oFB_photo_Bbox.addBbox(Bbox("4_Face", 758, 185, 1162, 589))
        oFB_photo_Bbox.addBbox(Bbox("4_Photo", 761, 604, 827, 698))
        oFB_photo_Bbox.addBbox(Bbox("4_Text", 832, 608, 1124, 708))
        oFB_photo_Bbox.addBbox(Bbox("4_Comment", 760, 715, 856, 755))
        oFB_photo_Bbox.addBbox(Bbox("4_LeftEmoji", 1152, 607, 1200, 642))
        dictOfInterfaceBbox["FB_photo"] = oFB_photo_Bbox

        oGmail_4_Bbox = InterfaceBbox("gmail_4")
        oGmail_4_Bbox.addBbox(Bbox("5_Title", 629, 165, 1320, 210))
        oGmail_4_Bbox.addBbox(Bbox("5_UnderTitle", 626, 214, 1318, 257))
        oGmail_4_Bbox.addBbox(Bbox("5_Text", 628, 270, 1316, 860))
        oGmail_4_Bbox.addBbox(Bbox("5_RightButtons", 1327, 265, 1384, 652))
        oGmail_4_Bbox.addBbox(Bbox("5_Send", 625, 864, 693, 898))
        oGmail_4_Bbox.addBbox(Bbox("5_Delete", 1280, 866, 1324, 898))
        dictOfInterfaceBbox["gmail_4"] = oGmail_4_Bbox

        oBlogger_7_Bbox = InterfaceBbox("Blogger_7")
        oBlogger_7_Bbox.addBbox(Bbox("6_Title", 625, 164, 1319, 212))
        oBlogger_7_Bbox.addBbox(Bbox("6_Text", 626, 234, 1322, 838))
        oBlogger_7_Bbox.addBbox(Bbox("6_Comments", 459, 241, 617, 321))
        oBlogger_7_Bbox.addBbox(Bbox("6_Privacy", 461, 352, 594, 453))
        oBlogger_7_Bbox.addBbox(Bbox("6_Photo", 1353, 159, 1465, 291))
        oBlogger_7_Bbox.addBbox(Bbox("6_BottomButtons", 1277, 844, 1325, 871))
        oBlogger_7_Bbox.addBbox(Bbox("6_Delete", 1502, 557, 1325, 871))
        dictOfInterfaceBbox["Blogger_7"] = oBlogger_7_Bbox

        oBlogger_Bbox = InterfaceBbox("Blogger")
        oBlogger_Bbox.addBbox(Bbox("7_Title", 625, 164, 1319, 212))
        oBlogger_Bbox.addBbox(Bbox("7_Text", 627, 262, 1322, 866))
        oBlogger_Bbox.addBbox(Bbox("7_Buttons", 628, 210, 1318, 258))
        oBlogger_Bbox.addBbox(Bbox("7_Photo", 1353, 165, 1474, 284))
        oBlogger_Bbox.addBbox(Bbox("7_Comments", 1348, 317, 1515, 416))
        oBlogger_Bbox.addBbox(Bbox("7_Privacy", 1360, 437, 1501, 540))
        dictOfInterfaceBbox["Blogger"] = oBlogger_Bbox

        oFB_post_Bbox = InterfaceBbox("FB_post")
        oFB_post_Bbox.addBbox(Bbox("8_Photo", 757, 469, 825, 540))
        oFB_post_Bbox.addBbox(Bbox("8_Text", 831, 467, 1204, 577))
        oFB_post_Bbox.addBbox(Bbox("8_Emoji", 1214, 468, 1251, 504))
        oFB_post_Bbox.addBbox(Bbox("8_Cancel", 756, 592, 850, 623))
        oFB_post_Bbox.addBbox(Bbox("8_Post", 1136, 592, 1207, 628))
        dictOfInterfaceBbox["FB_post"] = oFB_post_Bbox

        oBlogger_6_Bbox = InterfaceBbox("Blogger_6")
        oBlogger_6_Bbox.addBbox(Bbox("9_Title", 625, 164, 1319, 212))
        oBlogger_6_Bbox.addBbox(Bbox("9_Text", 626, 234, 1322, 838))
        oBlogger_6_Bbox.addBbox(Bbox("9_BottomButtons", 621, 835, 958, 877))
        oBlogger_6_Bbox.addBbox(Bbox("9_BottomRight", 1276, 837, 1323, 876))
        oBlogger_6_Bbox.addBbox(Bbox("9_Photo", 1345, 159, 1473, 285))
        oBlogger_6_Bbox.addBbox(Bbox("9_Comments", 1347, 318, 1506, 420))
        oBlogger_6_Bbox.addBbox(Bbox("9_Privacy", 1349, 443, 1502, 537))
        dictOfInterfaceBbox["Blogger_6"] = oBlogger_6_Bbox

        oGmail_1_Bbox = InterfaceBbox("gmail_1")
        oGmail_1_Bbox.addBbox(Bbox("10_Title", 629, 165, 1320, 210))
        oGmail_1_Bbox.addBbox(Bbox("10_UnderTitle", 626, 214, 1318, 257))
        oGmail_1_Bbox.addBbox(Bbox("10_Text", 628, 270, 1316, 860))
        oGmail_1_Bbox.addBbox(Bbox("10_LeftButtons", 558, 262, 624, 654))
        oGmail_1_Bbox.addBbox(Bbox("10_Send", 627, 866, 700, 902))
        oGmail_1_Bbox.addBbox(Bbox("10_Delete", 1279, 863, 1327, 899))
        dictOfInterfaceBbox["gmail_1"] = oGmail_1_Bbox

        oBlogger_9_Bbox = InterfaceBbox("Blogger_9")
        oBlogger_9_Bbox.addBbox(Bbox("11_Title", 625, 164, 1319, 212))
        oBlogger_9_Bbox.addBbox(Bbox("11_Buttons", 627, 210, 999, 252))
        oBlogger_9_Bbox.addBbox(Bbox("11_Delete", 1286, 212, 1326, 248))
        oBlogger_9_Bbox.addBbox(Bbox("11_Text", 625, 253, 1325, 857))
        oBlogger_9_Bbox.addBbox(Bbox("11_Photo", 446, 157, 585, 293))
        oBlogger_9_Bbox.addBbox(Bbox("11_Comments", 456, 319, 611, 419))
        oBlogger_9_Bbox.addBbox(Bbox("11_Privacy", 458, 437, 599, 532))
        dictOfInterfaceBbox["Blogger_9"] = oBlogger_9_Bbox

        oGmail_8_Bbox = InterfaceBbox("gmail_8")
        oGmail_8_Bbox.addBbox(Bbox("12_Title", 628, 163, 1325, 212))
        oGmail_8_Bbox.addBbox(Bbox("12_UnderTitle", 623, 218, 1322, 264))
        oGmail_8_Bbox.addBbox(Bbox("12_Buttons", 624, 263, 1121, 299))
        oGmail_8_Bbox.addBbox(Bbox("12_Delete", 1280, 270, 1327, 298))
        oGmail_8_Bbox.addBbox(Bbox("12_Text", 621, 305, 1320, 899))
        dictOfInterfaceBbox["gmail_8"] = oGmail_8_Bbox

        oDB_diary_8_Bbox = InterfaceBbox("DB_diary_8")
        oDB_diary_8_Bbox.addBbox(Bbox("13_Title", 628, 163, 1325, 212))
        oDB_diary_8_Bbox.addBbox(Bbox("13_UnderTitle", 623, 218, 1322, 264))
        oDB_diary_8_Bbox.addBbox(Bbox("13_Text", 625, 254, 1322, 856))
        oDB_diary_8_Bbox.addBbox(Bbox("13_Send", 625, 851, 706, 899))
        oDB_diary_8_Bbox.addBbox(Bbox("13_Cancel", 1242, 852, 1331, 896))
        dictOfInterfaceBbox["DB_diary_8"] = oDB_diary_8_Bbox

        oBlogger_8_Bbox = InterfaceBbox("Blogger_8")
        oBlogger_8_Bbox.addBbox(Bbox("14_Title", 622, 162, 1322, 218))
        oBlogger_8_Bbox.addBbox(Bbox("14_Buttons", 622, 218, 999, 251))
        oBlogger_8_Bbox.addBbox(Bbox("14_Delete", 1268, 216, 1339, 248))
        oBlogger_8_Bbox.addBbox(Bbox("14_Photo", 624, 253, 718, 361))
        oBlogger_8_Bbox.addBbox(Bbox("14_Comments", 722, 255, 891, 357))
        oBlogger_8_Bbox.addBbox(Bbox("14_Privacy", 898, 256, 1039, 358))
        oBlogger_8_Bbox.addBbox(Bbox("14_Text", 628, 363, 1322, 969))
        dictOfInterfaceBbox["Blogger_8"] = oBlogger_8_Bbox

        oGmail_4_Bbox = InterfaceBbox("gmail_4")
        oGmail_4_Bbox.addBbox(Bbox("15_Title", 627, 163, 1323, 213))
        oGmail_4_Bbox.addBbox(Bbox("15_UnderTitle", 629, 215, 1321, 265))
        oGmail_4_Bbox.addBbox(Bbox("15_Text", 623, 268, 1321, 868))
        oGmail_4_Bbox.addBbox(Bbox("15_Send", 618, 871, 706, 903))
        oGmail_4_Bbox.addBbox(Bbox("15_Delete", 1290, 870, 1328, 900))
        oGmail_4_Bbox.addBbox(Bbox("15_Buttons", 1326, 257, 1388, 667))
        dictOfInterfaceBbox["gmail_4"] = oGmail_4_Bbox

        oBlogger_10_Bbox = InterfaceBbox("Blogger_10")
        oBlogger_10_Bbox.addBbox(Bbox("16_Title", 622, 162, 1324, 215))
        oBlogger_10_Bbox.addBbox(Bbox("16_Buttons", 622, 217, 1000, 254))
        oBlogger_10_Bbox.addBbox(Bbox("16_Delete", 1275, 218, 1331, 254))
        oBlogger_10_Bbox.addBbox(Bbox("16_Text", 623, 255, 1321, 858))
        oBlogger_10_Bbox.addBbox(Bbox("16_Photo", 621, 860, 708, 971))
        oBlogger_10_Bbox.addBbox(Bbox("16_Comments", 725, 859, 880, 970))
        oBlogger_10_Bbox.addBbox(Bbox("16_Privacy", 902, 862, 1036, 962))
        dictOfInterfaceBbox["Blogger_10"] = oBlogger_10_Bbox

        oGitHub_8_Bbox = InterfaceBbox("GitHub_8")
        oGitHub_8_Bbox.addBbox(Bbox("17_Photo", 627, 153, 705, 232))
        oGitHub_8_Bbox.addBbox(Bbox("17_CommitMsg", 706, 159, 1285, 292))
        oGitHub_8_Bbox.addBbox(Bbox("17_Button1", 618, 289, 901, 322))
        oGitHub_8_Bbox.addBbox(Bbox("17_Button2", 618, 324, 851, 353))
        oGitHub_8_Bbox.addBbox(Bbox("17_Text", 625, 389, 1330, 800))
        oGitHub_8_Bbox.addBbox(Bbox("17_Commit", 622, 796, 774, 846))
        oGitHub_8_Bbox.addBbox(Bbox("17_Cancel", 775, 793, 858, 852))
        dictOfInterfaceBbox["GitHub_8"] = oGitHub_8_Bbox

        oBlogger_1_Bbox = InterfaceBbox("Blogger_1")
        oBlogger_1_Bbox.addBbox(Bbox("18_Title", 625, 165, 1318, 213))
        oBlogger_1_Bbox.addBbox(Bbox("18_Text", 628, 231, 1323, 840))
        oBlogger_1_Bbox.addBbox(Bbox("18_Photo", 450, 162, 555, 283))
        oBlogger_1_Bbox.addBbox(Bbox("18_Comments", 402, 320, 557, 418))
        oBlogger_1_Bbox.addBbox(Bbox("18_Privacy", 408, 439, 536, 545))
        oBlogger_1_Bbox.addBbox(Bbox("18_Delete", 409, 611, 456, 650))
        oBlogger_1_Bbox.addBbox(Bbox("18_Buttons", 556, 306, 625, 642))
        dictOfInterfaceBbox["Blogger_1"] = oBlogger_1_Bbox

        oAmazon_review_Bbox = InterfaceBbox("Amazon_review")
        oAmazon_review_Bbox.addBbox(Bbox("20_Photo", 609, 181, 765, 346))
        oAmazon_review_Bbox.addBbox(Bbox("20_Text", 773, 183, 1248, 393))
        oAmazon_review_Bbox.addBbox(Bbox("20_UnderTitle", 766, 393, 1248, 437))
        oAmazon_review_Bbox.addBbox(Bbox("20_Close", 771, 447, 853, 480))
        oAmazon_review_Bbox.addBbox(Bbox("20_Submit", 1163, 445, 1251, 489))
        dictOfInterfaceBbox["Amazon_review"] = oAmazon_review_Bbox

        oBlogger_11_Bbox = InterfaceBbox("Blogger_11")
        oBlogger_11_Bbox.addBbox(Bbox("21_Photo", 528, 167, 619, 232))
        oBlogger_11_Bbox.addBbox(Bbox("21_Title", 625, 166, 1324, 212))
        oBlogger_11_Bbox.addBbox(Bbox("21_Buttons", 618, 217, 996, 254))
        oBlogger_11_Bbox.addBbox(Bbox("21_Delete", 1271, 215, 1329, 243))
        oBlogger_11_Bbox.addBbox(Bbox("21_Text", 615, 258, 1323, 859))
        oBlogger_11_Bbox.addBbox(Bbox("21_Post", 622, 883, 695, 927))
        oBlogger_11_Bbox.addBbox(Bbox("21_Comments", 724, 865, 890, 968))
        oBlogger_11_Bbox.addBbox(Bbox("21_Privacy", 903, 862, 1037, 969))
        dictOfInterfaceBbox["Blogger_11"] = oBlogger_11_Bbox

        oGmail_8_Bbox = InterfaceBbox("gmail_8")
        oGmail_8_Bbox.addBbox(Bbox("22_Title", 622, 164, 1326, 213))
        oGmail_8_Bbox.addBbox(Bbox("22_UnderTitle", 620, 217, 1324, 262))
        oGmail_8_Bbox.addBbox(Bbox("22_Buttons", 624, 269, 1123, 297))
        oGmail_8_Bbox.addBbox(Bbox("22_Delete", 1274, 265, 1339, 299))
        oGmail_8_Bbox.addBbox(Bbox("22_Text", 624, 304, 1323, 899))
        dictOfInterfaceBbox["gmail_8"] = oGmail_8_Bbox

        oBlogger_3_Bbox = InterfaceBbox("Blogger_3")
        oBlogger_3_Bbox.addBbox(Bbox("23_Photo", 451, 162, 568, 298))
        oBlogger_3_Bbox.addBbox(Bbox("23_Comments", 453, 317, 615, 408))
        oBlogger_3_Bbox.addBbox(Bbox("23_Privacy", 453, 435, 599, 538))
        oBlogger_3_Bbox.addBbox(Bbox("23_Delete", 454, 548, 506, 589))
        oBlogger_3_Bbox.addBbox(Bbox("23_Title", 620, 163, 1329, 217))
        oBlogger_3_Bbox.addBbox(Bbox("23_Text", 625, 227, 1320, 835))
        oBlogger_3_Bbox.addBbox(Bbox("23_Buttons", 621, 838, 975, 880))
        oBlogger_3_Bbox.addBbox(Bbox("23_Something", 1287, 836, 1325, 869))
        dictOfInterfaceBbox["Blogger_3"] = oBlogger_3_Bbox

        oGitHub_Bbox = InterfaceBbox("GitHub")
        oGitHub_Bbox.addBbox(Bbox("24_Text", 621, 164, 1332, 568))
        oGitHub_Bbox.addBbox(Bbox("24_Photo", 612, 596, 702, 687))
        oGitHub_Bbox.addBbox(Bbox("24_CommitMsg", 706, 594, 1276, 737))
        oGitHub_Bbox.addBbox(Bbox("24_CommitBranch", 623, 737, 907, 767))
        oGitHub_Bbox.addBbox(Bbox("24_NewBranch", 622, 772, 856, 796))
        oGitHub_Bbox.addBbox(Bbox("24_Commit", 627, 797, 769, 841))
        oGitHub_Bbox.addBbox(Bbox("24_Cancel", 771, 803, 868, 837))
        dictOfInterfaceBbox["GitHub"] = oGitHub_Bbox

        oGmail_1_Bbox = InterfaceBbox("gmail_1")
        oGmail_1_Bbox.addBbox(Bbox("25_Title", 619, 167, 1331, 211))
        oGmail_1_Bbox.addBbox(Bbox("25_UnderTitle", 618, 216, 1321, 260))
        oGmail_1_Bbox.addBbox(Bbox("25_Text", 624, 264, 1321, 865))
        oGmail_1_Bbox.addBbox(Bbox("25_Send", 621, 869, 720, 903))
        oGmail_1_Bbox.addBbox(Bbox("25_Delete", 1283, 866, 1349, 902))
        oGmail_1_Bbox.addBbox(Bbox("25_Buttons", 557, 262, 618, 656))
        dictOfInterfaceBbox["gmail_1"] = oGmail_1_Bbox

        oBlogger_4_Bbox = InterfaceBbox("Blogger_4")
        oBlogger_4_Bbox.addBbox(Bbox("26_Title", 620, 166, 1320, 213))
        oBlogger_4_Bbox.addBbox(Bbox("26_Text", 611, 229, 1322, 837))
        oBlogger_4_Bbox.addBbox(Bbox("26_Photo", 1349, 164, 1466, 291))
        oBlogger_4_Bbox.addBbox(Bbox("26_Buttons", 1330, 309, 1389, 626))
        oBlogger_4_Bbox.addBbox(Bbox("26_Comments", 1399, 317, 1565, 420))
        oBlogger_4_Bbox.addBbox(Bbox("26_Privacy", 1402, 441, 1549, 524))
        dictOfInterfaceBbox["Blogger_4"] = oBlogger_4_Bbox

        oTumblr_link_Bbox = InterfaceBbox("Tumblr_link")
        oTumblr_link_Bbox.addBbox(Bbox("27_Photo", 697, 180, 766, 262))
        oTumblr_link_Bbox.addBbox(Bbox("27_Title", 779, 186, 1251, 234))
        oTumblr_link_Bbox.addBbox(Bbox("27_Text", 773, 239, 1251, 442))
        oTumblr_link_Bbox.addBbox(Bbox("27_Send", 758, 443, 862, 487))
        oTumblr_link_Bbox.addBbox(Bbox("27_Cancel", 1179, 454, 1255, 491))
        dictOfInterfaceBbox["Tumblr_link"] = oTumblr_link_Bbox

        return dictOfInterfaceBbox
