# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 17:31:49 2021

@author: Shweta
"""


import streamlit as st
import math
import pandas as pd
import numpy as np


menu = ["About","Beam","Slab"]
choice = st.sidebar.selectbox ("Menu",menu)
        
st.header ('RC Beam & Slab Design Application')   #check if this line can go in title
st.image("img_cbrilogo2.png", width = 120)

if choice == 'About':
    st.header ("About")
    st.write ("This application is developed to design and detail RC beams and slabs using Limit State Design as per Indian Standards (IS 456: 2000 and IS 13920: 2016).") 
    st.write ("Please select an option to start designing the respective structural component based on your inputs.")
    st.write ("** General materials, construction methods and safety shall be followed strictly. All responsibilities rest with the user.")
    
    
    
############Beam Page###################

if choice == 'Beam':
    st.header ("Beam")
    st.write ("Enter details:")
        
    bly = st.text_input("Longer span of slab supported by beam (m)", 0)    #helper_text: "(should be in m)"
    #here 0=default value. if you dont enter one then it will show warning on the app page 
    blx = st.text_input("Shorter span of slab supported by beam (m)", 0)   #helper_text: "(should be in m)"
    ts = st.text_input("Slab thickness (mm)", 0)   #helper_text: "(should be in mm)"
    bfck = st.text_input("Concrete grade (MPa)", 0)  #helper_text: "(should be in MPa)"
    bfy = st.text_input("Steel grade (MPa)", 0)      #helper_text: "(should be in MPa)"
    blv_load = st.text_input("Live load on slab supported by beam (kN/m^2)", 0)   #helper_text: "(should be in kN/m^2)"
    bfloor_fin = st.text_input("Floor finish on slab supported by beam (kN/m^2)", 0)   #helper_text: "(should be in kN/m^2)"
    bdia = st.text_input("Assumed longitudinal bar diameter (mm)", 0)  #helper_text: "(should be in mm)"
    
    bbs = st.selectbox ("Thickness of the wall (supported by the beam)", ('230 mm','115 mm','No wall'))   #helper_text: "(should be in mm)" #text: " (supported by the beam)"
    #first condition is the default condition        
    
    ans = st.selectbox ("Beam is along", ('Shorter Span','Longer Span'))        #first condition is the default condition     
    
    btype = st.selectbox ("Beam type", ('Intermediate','Edge'))                   #first condition is the default condition 


    if st.button ("Design"):
        #st.write ("Code comes here")  # Calculation + result
        #c = int(a) + int(b)
        #st.write ("Value of c is: ",c)   
       
        i = 1  
        bpt = 0.15
        while 0.15 <= float (bpt) <= 4:
        
            print ("\n\n\n\n")
            print ("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            print ("This is iteration number ", i)
        
            bpt = round(float(bpt),2)                                            # percentage
            print ("Percentage is", bpt)
            
            ib1 = math.log(bpt,10)                                               # calculate MF
            ib2 = float (bfy) * 0.58
            bMF = 1/ (0.225 + (0.00322 * ib2) + (0.625 * float(ib1)) )
            bMF = round (bMF,3)
            #bMF = 1
            print ('Modification Factor (MF) is: ',round(bMF,3))
            
            if ans == "Shorter Span":                                                    # if beam is along shorter span
                bL = float (blx)
            if ans == "Longer Span":
                bL = float (bly)
            else:
                print ("Invalid choice. \nEnter either '1' or '0'.")
            
            #Effective Depth (d)                                                           # (mm)
            bd = ((bL +0.46)*1000) / (20*bMF)                                        
            bd = round(bd,3)
            print ('Effective depth (d) is: ',bd)
                                                                        
            #Depth (D)(mm)
            bD = bd + 25 + (float(bdia)/2)
            bD = round(bD,3)
            print ("Depth is:", bD)
            # round up to +5 
            base = 5
            ib3 = int(bD/base)
            bD = (ib3 +1) * base
            print ('Depth (D) after rounding up is: ',bD)
        
            # Effective span (Le) (mm) (calculated only for the selected span i.e., either longer or shorter)
            bLe = bL + (bd/1000)
            bLe = round (bLe,3)
            print ('Effective span (Le) is: ',bLe)
            
            bWs = 0
            bww = 0
            bh = 0
   
            if bbs == "230 mm":
                bbs = 230
            if bbs == "115 mm":
                bbs = 115
            if bbs == "None":
                bbs = 0   
            
            bb = float (bbs)
            print ('b is:',float(bbs))
            
            if btype == "Intermediate":
                btype = "i1"
            if btype == "Edge":
                btype = "e1"
                
        
            #Distribute slab load on beam
            if ans == 0:                                                    #if beam is along shorter span
                print ("Beam is along shorter span:")
                if btype == "i1":
                    bWs = (float(blx) * (float(blx)/2) *  float(ts) * 25) / 1000 
                elif btype == 'e1':
                    bWs = ((float(blx) * (float(blx)/2) *  float(ts) * 25) / 1000) * 0.5
                print ("Ws for beam is:",round(bWs,3))                                                    #(kN) 
                bww = (float(bb)/1000) * 3 * 19
                bww = round(bww,2)
                print ('bww is: ',bww)
                ib60 = float(bfloor_fin) + float(blv_load)
                bh = float(blx) * (float(blx)/2) * ib60
                bh = round(bh,3)
                print ("h is:",bh)
            
            if ans == 1:                                                    #if beam is along longer span
                print ("Beam is along longer span:")
                if btype == "i1":
                    bWs = ((float(bly) + float(bly) - float(blx)) * (float(blx)/2) * float(ts) * 25) /1000             #weight of slab       #removed (* 0.5) 
                elif btype == 'e1':
                    bWs = (((float(bly) + float(bly) - float(blx)) * (float(blx)/2) * float(ts) * 25) /1000) * 0.5
                print ("Ws for beam is:",round(bWs,3))  #(kN)
                print ('b is:',float(bb))
                bww = (float(bb)/1000) * 3 * 19    
                bww = round(bww,2)
                print ('bww is: ',bww)
                ib60 = float(bfloor_fin) + float(blv_load)
                ib61 = float(bly) + float(bly) - float(blx)
                bh =  ib61 * (float(blx)/2) * ib60                                             # removed (* 0.5)
                bh = round(bh,3)
                print ("h is:",bh)
        
            #Calculate beam weight
            #Self weight of beam
            #bSW = (float(bb) * bD * 25)/1000000                                  #Self weight of beam   (kN/m)  # removed
            #bSW = round(bSW,3)
            #print ("Self weight of beam is:",bSW)
        
            #Total factored weight
            #bW = 1.5 * ((bWs/bL) + bSW + (bh/bL) + bww) 
            bW = 1.5 * ((bWs/bL) + (bh/bL) + bww) 
            bW = round(bW,3)
            #bW = 52.5
            print ("Total factored weight of beam is:",bW)                       #(kN/m)
         
            #Bending moment  (N-mm)
            bBM = ((bW*(float(bLe)**2))/ 8)                                    #shorter span yes   
            #round (bBM,3)
            print ('Bending Moment is: ',bBM )
            
            #Error management (which occurs in calculating intm4 for ast)           ######################  WHAT????????????
            #ib65 = 0.87 * (float(bfy)/200000)
            #e1 = (0.0035 * bd) / (0.0055 + ib65)
            #print ("e1 is: ", e1)
            #ib66 = bd - (0.416 * e1)
            #BM_lim = 0.362 * float(bfck) * e1 * float(bb) * ib66
            #BM_lim = round (BM_lim,3)
            #print ("e2 is: ", BM_lim)
            #BM_lim = 0.362 * float(bfck) * (0.0035 * bd) / (0.0055 + ib65) * float(bb) * bd - (0.416 * (0.0035 * bd) / (0.0055 + 0.87 * (float(bfy)/200000)))
            
            ib101 = 0.87 * (float(bfy)/200000)
            Xu_d = 0.0035 / (0.0055 + ib101)
            print ("Xu_d is:", Xu_d)
            
            #try:
            #    ib102 = (bBM * 1000 * 1000) / (0.362 * float(bfck) * Xu_d * float(bb))
            #except ZeroDivisionError:
            #    ib102 = (bBM * 1000 * 1000)                                  ###################################################ASK
            
            if float(bb)!= 230:
                bb = 230
                
                
            ib102 = (bBM * 1000 * 1000) / (0.362 * float(bfck) * Xu_d * bb)
            ib103 = math.sqrt(ib102)    
            ib104 = 1 - (0.416 * Xu_d)
            ib105 = math.sqrt(ib104)
            d2 = ib103 / ib105
        
            if bd > d2:                     #(greater value is selected from bd and d2)
                d2 = bd  
            else:
                d2 = d2
            print ("d2 is: ", d2)
            
            D2 = d2 + 25 + (float(bdia)/2)
            print ("D2 is: ", D2)
            
            if ((1.5*bb) > D2):
                D2 = 1.5*bb
            print ("Value of D2 when 1.5*bb: ", D2)
                
            if (D2%5 !=0):
                # round up to +5 
                base = 5
                ib31 = int(D2/base)
                D2 = (ib31 +1) * base
            print ('D2 after rounding up is: ',D2)
        
            
            d3 = D2 - 25 - (float(bdia)/2)
            print ("d3 is: ", d3)
            
            print ('b is:',float(bb))
                
            if bb < (0.35*d3):
                while bb < (0.35*d3):   
        
                    if (bb%5 !=0):
                        # round up b to +5 
                        base = 5
                        ib31 = int(bb/base)
                        bb = (ib31 +1) * base
                    print ('b after rounding up is: ',bb)  
        
                    ib102 = (bBM * 1000 * 1000) / (0.362 * float(bfck) * Xu_d * bb)
                    ib103 = math.sqrt(ib102)    
                    ib104 = 1 - (0.416 * Xu_d)
                    ib105 = math.sqrt(ib104)
                    d2 = ib103 / ib105
        
                    if bd > d2:                     #(greater value is selected from bd and d2)
                        d2 = bd  
                    else:
                        d2 = d2
                    print ("d2 is: ", d2)
        
                    D2 = d2 + 25 + (float(bdia)/2)
                    print ("D2 is: ", D2)
        
                    if ((1.5*bb) > D2):                  #maximum of D2 and d2*b
                        D2 = 1.5*bb
                        
                    if (D2%5 !=0):
                        # round up to +5 
                        base = 5
                        ib31 = int(D2/base)
                        D2 = (ib31 +1) * base
                    print ('D2 after rounding up is: ',D2)
        
                    d3 = D2 - 25 - (float(bdia)/2)
                    print ("d3 is: ", d3)
        
                    print ('b is:',float(bb))
        
                    #if float(bb) == 0:
                    #    bb = 0
                    #else: 
                    if bb < (0.35*d3):
                        bb = 0.35*d3
        
                    else:
                        print ("else me")
                        break
                        #bb = bb  
        
            print ('b after loop is:',bb)
            print ("d2 is: ",d2)
            print ("D2 is: ",D2)
            print ("d3 is: ",d3)
            
            #self wt 2
            SW2 = (bb * D2 * 25)/1000000
            #D2 * float(bb)
            SW2 = round(SW2,3)
            print ("SW2 is:",SW2)
        
            #Total factored weight 2
            W2 = 1.5 * ((bWs/bL) + SW2 + (bh/bL) + bww)                     
            W2 = round(W2,3)
            print ("TFW2 is:",W2)                       #(kN/m)
         
            #Bending moment  (N-mm)
            BM2 = ((W2*(float(bLe)**2))/ 8)                                    #shorter span yes   
            print ('BM2 is: ',BM2 )
            
            #Shear Force  (aka, Vu) (N)
            bSF = (W2 * float(bLe)* 1000)/2000                                       #shorter span yes
            bSF = round (bSF,3)
            print ('Shear Force is: ',bSF)     
            
            #Calculate ast and ast_min for defining the first condition
            
            #try:
            #    ib41 = (4.6 * BM2 * 1000000)/(float(bfck) * float(bb) * d3 * d3)          # Ru
            #except ZeroDivisionError:
            #    ib41 = (4.6 * BM2 * 1000000)          ###################################################ASK
            
            ib41 = (4.6 * BM2 * 1000000)/(float(bfck) * bb * d3 * d3)          # Ru
            print ('ib41 is:', ib41)
            
            err = 0
            try:
                ib42 = 1-ib41
                print ('ib42 is:', ib42)
                ib43 = math.sqrt(ib42)
                print ('ib43 is:', ib43)
        
            except ValueError:  
                err = 1
                print ("Errorrr")
                
            if err == 1:
                bpt = float (bpt) + 0.01
                print ("continued to beginning-------------------------------")
                continue
                
            ib5 = (bb * d3 * 0.5 * float(bfck)) / float(bfy)
            print ('ib5 is:', ib5)
            ast = ib5 * (1-ib43)  
            ast = round (ast,3)      #ast (mm2)
            print ('ast is: ',ast)
            
            
            #ast_min (mm2)
            ast_min  = (0.85 * bb * d3) / float(bfy)  
            ast_min = round (ast_min,3)
            print ('ast_min is: ',ast_min)   
            
            if ast_min > ast:
                ast_select = ast_min
            else: 
                ast_select = ast
                
            #Step6: Number of rebars
            n = ast_select / (3.14 * (float(bdia)/2) * (float(bdia)/2))
            n = math.ceil(n)
            if n < 2:
                n = 2
            print ("n is: ",n)                                                   #If n is in decimal, roundup n to +1.
               
            astp = n * 3.14 * (float(bdia)/2) * (float(bdia)/2)
            print ("astp is: ",round(astp,3))
        
            btou_v = (bSF*1000)/ (d3 * bb)
            btou_v = round(btou_v,3)
            print ('tou_v is: ', btou_v)
        
            ib7 = (0.116 * float(bfck) * bb * d3)/ (100 * astp)
            print ("ib7 is:", ib7)
            if ib7 > 1.0 :
                bB = ib7
            else : 
                bB = 1.0
            #print (B)
        
            ib8 = math.sqrt(0.8 * float(bfck))
            print ("ib8 is:",ib8)
            ib9 = math.sqrt(1+(5 * bB))
            print ("ib9 is:",ib9)
            btou_c = (0.85 * ib8 * (ib9 - 1)) /  (6*bB)
            btou_c = round(btou_c,3)
            print ('tou_c is: ',btou_c)
            
            
            if btou_c > btou_v:
                while btou_c > btou_v:
                    astp = astp - 10
                    print ("10 subtracted from astp. Now astp is: ", astp)
                    ib7 = (0.116 * float(bfck) * float(bb) * d3)/ (100 * astp)
                    #print ("ib7 is:", ib7)
                    if ib7 > 1.0 :
                        bB = ib7
                    else : 
                        bB = 1.0
                    #print (B)
        
                    ib8 = math.sqrt(0.8 * float(bfck))
                    #print ("ib8 is:",ib8)
                    ib9 = math.sqrt(1+(5 * bB))
                    #print ("ib9 is:",ib9)
                    btou_c = (0.85 * ib8 * (ib9 - 1)) /  (6*bB)
                    btou_c = round(btou_c,3)
                    print ('tou_c is: ',btou_c)
                    
                    if btou_v > btou_c:
                        break
                    
        
            if btou_v > btou_c:                                       #ast > ast_min and
                #btou_c > btou_v and
                #and intm4 != 0.0001
                print ("Both conditions satisfied")                # all output print statements go here
                
                #PRINT STATEMENTS
                
                break
                #elif ib4 == 0.0001:
                #print ("elif me aaya")
                #bpt = float (bpt) + 0.01
                #i = i+1    
            else:
                print ("else me")
                bpt = float (bpt) + 0.01
                i = i+1
                
                
        VSF = ((bSF*1000) - (btou_c * bb * d3)) / 1000
        VSF = round(VSF,3)
        print ("VSF is: ",VSF)                                                               #(N)
        
        #Calculate spacing (bspace):
        bspace = ((0.87 * float(bfy) * 3.14 * 16 * d3)/ (VSF*1000)) *2                                
        bspace = round(bspace,3)  
        print ("Spacing is: ",bspace)                                                        #(mm)
        #Round down s to -5 mm = spro             
        base = 5   # base
        ib50 = int(bspace/base)
        #print ("intm50 is:", intm50)
        spro = ib50 * base
        print ('spro (i.e., after rounding down) is: ',spro)  
        
        #Asv
        asv = (3.14 * 16 * float(bfy)) / (0.4 * bb)
        print ('asv is: ',asv)
        
        #if (spro > 200) and (asv > 200) :
        #    #Calculate spacing again (bspace):
        #    bspace2 = (0.87 * float(bfy) * 3.14 * 9 * d3)/ (VSF*1000)                     # 16 is changed to 9                    
        #    bspace2 = round(bspace2,3)  
        #    print ("Spacing is: ",bspace2)                                                        #(mm)
        #    #Round down s to -5 mm = spro             
        #    base = 5   # base
        #    ib50 = int(bspace2/base)
        #    #print ("intm50 is:", intm50)
        #    spro2 = ib50 * base
        #    print ('spro2 (i.e., after rounding down) is: ',spro2)  
            
            #Asv
            #asv2 = (3.14 * 9 * float(bfy)) / (0.4 * float(bb))                            # 16 is changed to 9 
            #print ('asv2 is: ',asv2)
        
            
        sn1 = D2/4
        print ("D2/4 is: ", sn1)
        sn2 = 8*float(bdia)
        print ("8*dia is: ", sn2)
        sn3 = 100
        print ("100 is: ", sn3)
        list2 = [sn1,sn2,sn3]
        sort_list2 = np.sort(list2)
        print (list2)
        print(sort_list2)
        snext = sort_list2[0]                                        #this is also a spacinghence we'll round it down 
        print ("snext is: ", snext)
        #Round down s to -5 mm              
        base = 5   # base
        ib50 = int(snext/base)
        #print ("intm50 is:", intm50)
        snext = ib50 * base
        print ('snext (i.e., after rounding down) is: ',snext)  
        print("\n")
        
        #Condition: spro < 0.75*d3 and 450 and asv.                       #select min from spro,0.75*d,450,asv 
        
        list = [0.75*d3, 450, spro, asv]
        sort_list = np.sort(list)
        print (list)
        print(sort_list[0]) #minimum element
        mins = sort_list[0]
        
        #if spro < 0.75*d3:
        #    mins = spro
        #else: 
        #    mins = 0.75 * d3 
        #print ("mins 1st condition is: ", mins)
        
        #if mins > 450:
        #    mins = 450  
        print ("minimum of spro,asv,450 and 0.75*d is: ", mins) 
        
        #Round down mins to -5 mm 
        base = 5   # base
        ib50 = int(mins/base)
        #print ("intm50 is:", intm50)
        mins = ib50 * base
        print ('mins (i.e., after rounding down) is: ',mins)  
        print("\n")
        
        
        st.subheader ('INPUTS:')
        #self.root.ids.res201.text = str("Longer Span (m): " + str(res)) 
        st.write ("Longer Span (m): " + str(bly))                      
        st.write ("Shorter Span (m): " + str(blx))                          
        st.write ("Concrete Grade (MPa): " + str(bfck))
        st.write ("Steel Grade (MPa): " + str(bfy))                              
        st.write ("Live Load (kN/m2): " + str(blv_load))                                    
        st.write ("Floor Finish (kN/m2): " + str(bfloor_fin))

        st.subheader ("OUTPUTS:")                                   

        D2 = int(D2)
        bb = int(bb)
        n1 = 0.6 * n
        n1 = round (n1)
        n2 = 0.5 * n
        n2 = round (n2)
        beam_temp1 = int(2*D2)
    
        st.write ("Provide " + str(bb) + " X " + str(D2) + " mm beam section.") 
        
        st.write ("Bottom (Tension) Reinforcement:") 
        st.write ("Provide" + str(n) + " - " + str(bdia) + " mm at mid-span.")
        st.write ("Provide" + str(n1) + " - " + str(bdia) + " mm at end-span.")
        st.write ("Top (Compression) Reinforcement:")   
        st.write ("Provide" + str(n2) + " - " + str(bdia) + " mm at mid-span.")
        st.write ("Provide" + str(n) + " - " + str(bdia) + " mm at end-span.")
        
        st.write ("Provide 2 legged 8 mm dia stirrups @ " + str(mins) + " mm c/c at mid-span.")
        st.write ("Provide 2 legged 8 mm dia stirrups @ " + str(snext) + " mm c/c at end span upto " + str(beam_temp1) + " mm from the column edge.")   
        st.write ('Provide 25 mm clear cover to the reinforcement.')
        
        st.subheader ("Typical Reinforcement Detailing")   #for figure
        st.image("img_beam_app.png", width = 500)  #caption= "Typical Reinforcement Detailing in Beams",
        
        st.write ("")
        st.write ("NOTES:")
        st.write ("1. Design of beam incorporates effect of all the boundary conditions.")
        st.write ("2. Cover to enforcement is 25mm.")
        st.write ("3. Assume that adequate quality control and safety is obtained in casting and placement of reinforcement.")
        st.write ("4. Ductile detailing in beam shall be as per 'IS 13920: 2016'.")
        st.write ("5. Kindly refer to the following figure for typical reinforcement detailing in beams.")
                    
                    
        
        
        
        
     
        
        
        


################   SLAB   #################
        

elif choice == 'Slab':
    st.header ("Slab")
    st.write ("Enter details:")
        
    ly = st.text_input("Longer span (m)", 0)    #helper_text: "(should be in m)"
    #here 0=default value. if you dont enter one then it will show warning on the app page 
    lx = st.text_input("Shorter span (m)", 0)   #helper_text: "(should be in m)"
    fck = st.text_input("Concrete grade (MPa)", 0)  #helper_text: "(should be in MPa)"
    fy = st.text_input("Steel grade (MPa)", 0)      #helper_text: "(should be in MPa)"
    lv_load = st.text_input("Live load (kN/m^2)", 0)   #helper_text: "(should be in kN/m^2)"
    floor_fin = st.text_input("Floor finish (kN/m^2)", 0)   #helper_text: "(should be in kN/m^2)"
    dia = st.text_input("Assumed rebar diameter (bottom) (mm)", 0)  #helper_text: "(should be in mm)"
    dia2 = st.text_input("Assumed rebar diameter (top) (mm)", 0)   #helper_text: "(should be in mm)"
            
    sel = st.selectbox ('Select option',('Interior Panels',
                                               'One Short Edge Discontinuous',
                                               'One Long Edge Discontinuous',
                                               'Two Adjascent Edges Discontinuous',
                                               'Two Short Edges Discontinuous',
                                               'Two Long Edges Discontinuous',
                                               'Three Edges Discontinuous (One Long Edge Continuous)',
                                               'Three Edges Discontinuous (One Short Edge Continuous)',
                                               'Four Edges Discontinuous',
                                               'One-Way Slab'))   #first condition is the default condition
            
            # MDDropDownItem:
            #             id: menu1
            #             pos_hint: {'center_x': .5, 'center_y': .5}
            #             text: 'Select Option'
            #             on_release: app.menu.open()
            
    if st.button ("Design"):
        #st.write ("Code comes here")  
        
        
        if sel == 'Interior Panels':
            sel = 1
        if sel == 'One Short Edge Discontinuous':
            sel = 3
        if sel == 'One Long Edge Discontinuous':
            sel = 5
        if sel == 'Two Adjascent Edges Discontinuous':
            sel = 7
        if sel == 'Two Short Edges Discontinuous':
            sel = 9
        if sel == 'Two Long Edges Discontinuous':
            sel = 11
        if sel == 'Three Edges Discontinuous (One Long Edge Continuous)':
            sel = 13
        if sel == 'Three Edges Discontinuous (One Short Edge Continuous)':
            sel = 15
        if sel == 'Four Edges Discontinuous':
            sel = 17
        if sel == 'None':
            sel = 1

        print (sel)                     # do sel = y thing where reqd
        y = int(sel)
        
      
        #insert code
        
        def find_alpha_values(i_ratio,y):   #pass argument: value of x (longer span/shorter span)
        
            data1 = pd.read_csv('slabs_alpha3.csv')

            #data1.replace(0, NaN)
            #print ('\n')
            #i_ratio = 1.2         # will be determined through calculations       # columns
            x = str(i_ratio)
            print ("Longer span by shorter span (x) is:", float(x))
            
            #y = 7              # user defined condition                        # rows
            #print ("Enter condition number from the table (should be from 0 to 17).")
            #y = input()
        
            #t = 'alpha_y'       # pre- determined / rule
        
            # checking if the calculated ly/lx value exists in table columns  
            for col in data1.columns:
                if col == x:
                    #print ('hi')
                    cond1='true'
                    break
                else:
                    cond1 = 'false'
            
            if cond1 == 'true':
                #print('if me aaya')
                print('Take Alpha_x, Alpha_y directly from the table.\n')
                a_x = data1[str(x)][int(y)]
                if a_x == 0.00001:
                    a_x = 0
                print ('Alpha_x is:',round(a_x,4))
                a_y = data1['alpha_y'][int(y)]
                if a_y == 0.00001:
                    a_y = 0
                print ('Alpha_y is:',round(a_y,4))    
            
            if cond1 == 'false':
                #print('else me aaya')
                print ('Interpolate to get Alpha_x and take Alpha_y from table.\n')
                a_y = data1['alpha_y'][int(y)]
                if a_y == 0.00001:
                    a_y = 0
                print ('Alpha_y is:',round(a_y,4))
                print ('\n')
            
                # find all values for interpolation formula: 
                #1. 2 column names    
                #2. 2 cell values corresponding to those columns
            
                if 1.5 < float(x) and float(x) < 1.75:
                    #print ("internal If 1 me aaya")
                    prev_x = 1.5
                    print ('Previous column name is: ',str(prev_x))
                    ax_prev = data1[str(prev_x)][int(y)]
                    if ax_prev == 0.00001:
                        ax_prev = 0
                    print ('Value in previous column is:',round(ax_prev,3))
        
                    next_x = 1.75
                    print ('Next column name is: ',str(next_x))
                    ax_next = data1[str(next_x)][int(y)]
                    if ax_next == 0.00001:
                        ax_next = 0
                    print ('Value in next column is:',round(ax_next,3))
        
        
                if 1.75 < float(x) and float(x) <= 2:
                    #print ("internal If 2 me aaya")
                    prev_x = 1.75
                    print ('Previous column name is: ',str(prev_x))
                    ax_prev = data1[str(prev_x)][int(y)]
                    if ax_prev == 0.00001:
                        ax_prev = 0
                    print ('Value in previous column is:',round(ax_prev,3))
        
                    next_x = 2
                    print ('Next column name is: ',str(next_x))
                    ax_next = data1[str(next_x)][int(y)]
                    if ax_next == 0.00001:
                        ax_next = 0
                    print ('Value in next column is:',round(ax_next,3))
        
                if 1.0 <= float(x) and float(x) < 1.5:
            
                    ##print ("internal Else me aaya")
                    intm101 = float(x) * 10
                    ##print (intm101)
            
                    floor_x = math.floor(intm101)
                    ##print (floor_x)
                    prev_x = floor_x / 10
                    if prev_x == 1.0:
                        prev_x = int (1)
                        #print ("prev_x is:", prev_x)
                    print ('Previous column name is: ',str(prev_x))
                    ax_prev = data1[str(prev_x)][int(y)]
                    if ax_prev == 0.00001:
                        ax_prev = 0
                    print ('Value in previous column is:',round(ax_prev,3))
                
                    ceil_x = math.ceil(intm101)
                    ##print (ceil_x)
                    next_x = ceil_x / 10
                    print ('Next column name is: ',str(next_x))
                    ax_next = data1[str(next_x)][int(y)]
                    if ax_next == 0.00001:
                        ax_next = 0
                    print ('Value in next column is:',round(ax_next,3))
        
                # start interpolation formula
                h = next_x - prev_x 
                print ('h in interpolation is: ',round(h,2))
                p = (float(x) - prev_x) / (round(h,2))
                print ('p in interpolation is: ',round(p,2))
                ax_0 = ax_next - ax_prev
                print (round(ax_0,5))
                ##print (p * ax_0)
                a_x = ax_prev + round((p * ax_0),5)
                print ('Alpha_x is: ',round(a_x,4))              # required value of alpha for calculating bending moment
                print ('\n\n\n')
                
            return (round(a_x,4),round(a_y,4))
        
        # main program

        i = 1
        pt = 0.12
        while 0.12 <= float (pt) <= 1.50 :
            
            print ("\n\n\n\n")
            print ("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            
            print ("This is iteration number ", i)
            
            
            print ("pt is: ",pt)
            #step1 
            
            ptr = round (float(pt),2)
            print ("ptr is", ptr)
            
            
            intm1 = math.log(ptr,10)
            intm2 = float (fy) * 0.58
            MF = 1/ (0.225 + (0.00322 * intm2) + (0.625 * float(intm1) ) )
            MFr = round (MF,3)
            
            print ('MF is: ',MFr)
        
            #step2
            # Effective depth 
            #d = D-(15-(float(dia)/2))  
            d = float (lx) / ((20*MFr) - 1)                    #shorter span yes    #d unit = m
            print ('Effective depth (d) is: ',round (d*1000,3))    ## we multiply d by 1000 only for printing purpose 
            
            #depth
            #intm51 = float(lx) / (20 * MF)
            #D = intm51 + (float(dia)/2) + 15
            D = d + 0.015 + (float(dia)/2000)
            print ('Depth (D) is: ',round(D,3))
            D = round(D,3)
            #if not (round(D,3)%5) == 0:
            # round up
            base = 5
            intm3 = D * 1000
            print (intm3)
            if (intm3%5 !=0):
                intm3_1 = int(int(intm3)/base)
                intm3_2 = (intm3_1 +1) * base
                print (intm3_2)
                D = float(intm3_2)/1000
            print ('Depth (D) after rounding up is: ',D*1000)     ## for printing we multiply D by 1000 but actually it is only D and the value 'D' goes into the formula, and not valur 'D * 1000'
        
            #Effective span 
            Lx = float(lx) + d                                  #shorter span yes
            print ('Effective shorter span (L) is: ',round (Lx,3))
            
            Ly = float(ly) + d
            print ('Effective longer span (L) is: ',round (Ly,3)) 
        
        
            #step3
        
            # Self weight of slab
            SW = D * 25                                               # unit =(kN/m)
            print ('Self Weight (SW) of slab is (kN/m2): ', round(SW,3))
        
            # Total factored weight 
            W = 1.5*(SW + float(lv_load) + float(floor_fin))
            print ('Total factored weight (W) is (kN/m2): ',round (W,3))
            
        
            #step4
            # Bending moment
            i_ratio1 = round (Ly,3)/round (Lx,3)                            #longer span \ shorter span
            i_ratio = round (i_ratio1,2)
            if i_ratio == 1.0:
                i_ratio = 1
                #print ("i_ratio is:", round (i_ratio1,2))
            if i_ratio == 2.0:
                i_ratio = 2
            
            print ("i_ratio is:", round (i_ratio1,2))
            
            if float(i_ratio) > 2:                                      
                BM = (W*(float(Lx)**2))/ 8                             #shorter span yes
                print ('Bending Moment is: ', round (BM,3))            #(for bottom)
                
                #step5
                #ast_main                                              # only one ast is calculated, ie, ast_main
                intm4 = (4.6*BM*1000*1000)/ (float(fck)*1000*d*d*1000*1000)
                print ("intm4 is:",intm4)
                intm41 = 1 - intm4
                print ("intm41 is:",intm41)
                if intm41 < 0:
                    intm41 = 0.0001
                intm42 = math.sqrt(intm41)
                print ("intm42 is:",intm42)
                ast_main = (1000*1000*d*0.5*float(fck)) / float(fy)  * (1 - intm42)                   # for bottom
                print ('ast_main is: ',round (ast_main,3))
        
                s_main = (1000*3.14*float(dia)*float(dia) ) / (4 * ast_main)    
                print ('s_main is:',round (s_main,3))
                if s_main > (3*d*1000):
                    s_main = 3*d*1000
                # round down 
                base = 5   # base
                intm50 = int(s_main/base)
                #print ("intm50 is:", intm50)
                s_main = intm50 * base
                print ('s_main after rounding down is (BM): ',s_main)
        
                pt_new = (100* ast_main) / (s_main*d)
                print ('pt_new is: ',round (pt_new,3))
                
                intm5 = math.log(pt_new,10)
                intm6 = float (fy) * 0.58
                MF_new = MF = 1/ (0.225 + (0.00322* intm6 + (0.625* intm5)))
                print ('MF_new is: ', round (MF_new,3))
                
                
                #2. ast_dis2                                           # for bottom
                ast_dis2 = 0.0015 * 1000 * D * 1000
                print ('ast_dis2 is: ',round (ast_dis2,3))
                
                s_dis2 =(1000* 3.14* float(dia)* float(dia))/(4 * ast_dis2)  
                print ("s_dis2 is: ", round(s_dis2,3))
                if s_dis2 > (3*d*1000):
                    s_dis2 = 3*d*1000
                # round down 
                base = 5   # base
                intm50 = int(s_dis2/base)
                #print ("intm50 is:", intm50)
                sr_dis2 = intm50 * base
                print ('s_dis2 after rounding down is: ',sr_dis2)
                
                
                #2. ast_dis_top                                         # for top
                ast_dis_top = 0.0015 * 1000 * D * 1000
                print ('ast_dis2 is: ',round (ast_dis_top,3))
                
                s_dis_top =(1000* 3.14* float(dia2)* float(dia2))/(4 * ast_main)         # replaced ast_dis2 by ast_main as suggested by sir 12/9/2020
                print ("s_dis2 is: ", round(s_dis_top,3))
                if s_dis_top > (3*d*1000):
                    s_dis_top = 3*d*1000
                # round down 
                base = 5   # base
                intm50 = int(s_dis_top/base)
                #print ("intm50 is:", intm50)
                sr_dis_top = intm50 * base
                print ('s_dis2 after rounding down is: ',sr_dis_top)
                
            
            if float(i_ratio) < 2:                         #longer span \ shorter span
                
                print ("Refer to table for values of alpha:")
                # write function to retrieve 2 values of alpha
                
                #y = int(sel)
                print("y now is:", y)
            
                res = find_alpha_values(i_ratio,y)
                
                Alpha_x = res[0]
                print ('Value of Alpha_x (outsidefunction) is: ',Alpha_x)
                Alpha_y = res[1]
                print ('Value of Alpha_y (outsidefunction) is: ',Alpha_y)
                
                BMx = Alpha_x * W * (float(Lx)**2)              #shorter span yes          unit=kN m/m
                BMy = Alpha_y * W * (float(Lx)**2)              #longer span yes
                
                print ('Bending Moment corresponding to shorter span (BMx) and positive moment is: ', round (BMx,3))
                print ('Bending Moment corresponding to longer span (BMy) and positive moment is: ', round (BMy,3))
                
                print ('\n')
                
                BMx_neg = Alpha_x * 1.33 * W * (float(Lx)**2)              #shorter span yes          unit=kN m/m
                BMy_neg = Alpha_y * 1.33 * W * (float(Lx)**2)              #longer span yes
                
                print ('Bending Moment corresponding to shorter span (BMx) and negative moment is: ', round (BMx_neg,3))
                print ('Bending Moment corresponding to longer span (BMy) and negative moment is: ', round (BMy_neg,3))
                
                print ('\n')
                
                #step5
                
                # now 3 ast will be calculated 1. ast_main (formula based on BMx),
                #                              2. ast_dis1 (same formula as ast_main but using BMy)
                #                              3. ast_dis2 (different formula - bending moment is not required) 
                # Max value between ast_dis1 and ast_dis2 will be selected as ast_dis for further calculations
                
                
                
                #0. ast_mins                                       
                ast_mins = 0.0012 * 1000 * D * 1000
                print ('ast_mins is: ',round (ast_mins,3))
                
                s_mins =(1000* 3.14* float(dia2)* float(dia2))/(4 * ast_mins)  
                print ("s_mins is: ", round(s_mins,3))
                if s_mins > (3*d*1000):
                    s_mins = 3*d*1000
                # round down 
                base = 5   # base
                intm50 = int(s_mins/base)
                #print ("intm50 is:", intm50)
                sr_mins = intm50 * base
                print ('s_mins after rounding down is: ',sr_mins)
                
                
                
                
                
                # 1. ast_main
                intm4 = (4.6*BMx)/ (float(fck)*1000*d*d)  
                intm41 = 1-intm4
                if intm41 < 0:
                    intm41 = 0.0001
                print ("intm41 is:",intm41)
                ast_main = (1000*1000*d*0.5*float(fck)) / float(fy)  * (1-(math.sqrt (intm41)))
                if ast_mins > ast_main:
                    ast_main = ast_mins
                print ('ast_main is (corresponding to BMx): ',round (ast_main,3))
                
                try:
                    s_main = (1000*3.14*float(dia)*float(dia) ) / (4 * ast_main) 
                except ZeroDivisionError:
                    s_main = 0
                print ('s_main is (BMx):',round (s_main,3))
                if s_main > (3*d*1000):
                    s_main = 3*d*1000
                # round down 
                base = 5   # base
                intm50 = int(s_main/base)
                #print ("intm50 is:", intm50)
                s_main = intm50 * base
                print ('s_main after rounding down is (BMx): ',s_main)
                s_main = round (s_main,3)
                
                try:
                    pt_newa = (100* ast_main) / (s_main*d)
                except ZeroDivisionError:
                    pt_newa = 0
                print ('pt_new is: ',round (pt_newa,3))
                
                
                
                # 2. ast_dis1
                intm4 = (4.6*BMy)/ (float(fck)*1000*d*d)  
                intm41 = 1-intm4
                if intm41 < 0:
                    intm41 = 0.0001
                print ("intm41 is:",intm41)
                ast_dis1 = (1000*1000*d*0.5*float(fck)) / float(fy)  * (1-(math.sqrt (intm41)))
                if ast_mins > ast_dis1:
                    ast_dis1 = ast_mins
                print ('ast_dis1 is (corresponding to BMy): ',round (ast_dis1,3))
        
                try:
                    s_dis1 = (1000*3.14*float(dia)*float(dia) ) / (4 * ast_dis1)  
                except ZeroDivisionError:
                    s_dis1 = 0
                print ('s_dis1 is (BMy):',round (s_dis1,3))
                if s_dis1 > (3*d*1000):
                    s_dis1 = 3*d*1000
                # round down 
                base = 5   # base
                intm50 = int(s_dis1/base)
                #print ("intm50 is:", intm50)
                sr_dis1 = intm50 * base
                print ('s_dis2 after rounding down is (BMy): ',sr_dis1)
                
                try:
                    pt_newb = (100* ast_dis1) / (s_dis1*d)
                except ZeroDivisionError:
                    pt_newb = 0
                print ('pt_new is: ',round (pt_newb,3)) 
                
                
                # 3. ast_main for negative moment
                intm11 = (4.6*BMx_neg)/ (float(fck)*1000*d*d) 
                intm12 = 1-intm11
                if intm12 < 0:
                    intm12 = 0.0001
                print ("intm12 is:",intm12)
                ast_main_neg = (1000*1000*d*0.5*float(fck)) / float(fy)  * (1-(math.sqrt (intm12)))
                if ast_mins > ast_main_neg:
                    ast_main_neg = ast_mins
                print ('ast_main is (corresponding to BMx): ',round (ast_main_neg,3))
        
                try:
                    s_main_neg = (1000*3.14*float(dia2)*float(dia2) ) / (4 * ast_main_neg)    # dia for top 
                except ZeroDivisionError:
                    s_main_neg = 0
                print ('s_main is (BMx):',round (s_main_neg,3))
                if s_main_neg > (3*d*1000):
                    s_main_neg = 3*d*1000
                # round down 
                base = 5   # base
                intm50 = int(s_main_neg/base)
                #print ("intm50 is:", intm50)
                s_main_neg = intm50 * base
                print ('s_main after rounding down is (BMx): ',s_main_neg)
                
                s_main_neg = round (s_main_neg,3)
        
                # 2. ast_dis1 for negative moment
                intm13 = (4.6*BMy_neg)/ (float(fck)*1000*d*d)   
                intm14 = 1-intm13
                if intm14 < 0:
                    intm14 = 0.0001
                print ("intm14 is:",intm14)
                ast_dis1_neg = (1000*1000*d*0.5*float(fck)) / float(fy)  * (1-(math.sqrt (intm14)))
                if ast_mins > ast_dis1_neg:
                    ast_dis1_neg = ast_mins
                print ('ast_dis1 is (corresponding to BMy): ',round (ast_dis1_neg,3))
        
                try:
                    s_dis1_neg = (1000*3.14*float(dia2)*float(dia2) ) / (4 * ast_dis1_neg)    #dia for top
                except ZeroDivisionError:
                    s_dis1_neg = 0
                print ('s_dis1 is (BMy):',round (s_dis1_neg,3))
                if s_dis1_neg > (3*d*1000):
                    s_dis1_neg = 3*d*1000
                # round down 
                base = 5   # base
                intm50 = int(s_dis1_neg/base)
                #print ("intm50 is:", intm50)
                sr_dis1_neg = intm50 * base
                print ('s_dis2 after rounding down is (BMy): ',sr_dis1_neg)
               
                if pt_newa > pt_newb:
                    pt_new = pt_newa
                else:
                    pt_new = pt_newb
            
                intm5 = math.log(pt_new,10)
                intm6 = float (fy) * 0.58
                MF_new = 1/ (0.225 + (0.00322* intm6 + (0.625* intm5)))
                print ('MF_new is: ', round (MF_new,3))
            
                    
            print ("nunu")           
                       
            #step6           
            # Shear force                        #Shear Force is same for both conditions since it does not depend on BM
            SF = (W*float(lx))/2                            #shorter span yes
            print ('Shear Force is: ',round (SF,3))
        
                       
            ########### step6 Checking
                
            #part 1
        
            #ld_max = 20* MF_new
            #print ('ld_max is: ', round (ld_max,3))
            #ld_pro = L/d
            #print ('ld_pro is:', round (ld_pro,3))
            
            
            
            try:
                ast_latest = 3.14 * (float(dia)/2) * (float(dia)/2) * (1000/round(s_main,3)) 
            except ZeroDivisionError:
                ast_latest = 0
            print ('ast_latest is:', round (ast_latest,3))
            
            d_new = (D*1000) - 15 - (float(dia)/2)
            print ('d_new is:', round (d_new,3))
            
            pt_latest = (100 * round(ast_latest,3)) / (1000* round (d_new,3))
            print ('pt_latest is: ', round (pt_latest,3))
            
            
            try:
                intm90 = math.log(float(pt_latest),10)
                intm91 = float(fy) * 0.58
                MF_latest = 1/ (0.225 + (0.00322* intm91 + (0.625* intm90)))
                print ('MF_latest is: ', round (MF_latest,3))
            
                d_latest = ((float(lx)*1000) + d_new)/ (20*round (MF_latest,3))
                print ('d_latest is: ', round (d_latest,3))
                
            except ValueError:
                d_latest = 0
                print ('d_latest is: ', d_latest)
            
            
        
            #part 2
        
            # stress = shear force/ effective depth
            tou_v = SF/(d*1000)
            print ('tou_v is: ', round(tou_v,3))
        
            b = 1000
            
            try:
                intm7 = (0.116 * float(fck) * b * d *1000)/ (100*ast_main)
            except ZeroDivisionError:
                intm7 = 0
                
        
            if intm7 > 1.0 :
                B = intm7
            else : 
                B = 1.0
              
            #print (B)
        
            intm8 = math.sqrt(0.8 * float(fck))
            intm9 = math.sqrt(1+(5*B)) 
        
            tou_c = (0.85 * intm8 * (intm9 - 1)) /  (6*B)
            print ('tou_c is: ', round(tou_c,3))
            
            
        ############################### CONDITION ###################### 
            if tou_c > tou_v and round (d_latest,3) < round (d_new,3) :
                
                
                
                #print ("\n\n\n\n")
                #print ("---------------------------------------------------------------")
                st.subheader ("INPUTS:")                                              # add label inputs at top
                st.write ("Longer Span (m): " + str(ly))                      #
                st.write ("Shorter Span (m): " + str(lx))                          #
                st.write ("Concrete Grade (MPa): " + str(fck))
                st.write ("Steel Grade (MPa): " + str(fy))                              
                st.write ("Live Load (kN/m2): " + str(lv_load))                                    
                st.write ("Floor Finish (kN/m2): " + str(floor_fin))                                   
                # print ('\n')
                # print ("---------------------------------------------------------------")
                
                
                st.subheader ("OUTPUTS:")
                
                DDepth = int(D*1000)
                st.write ("Total Depth (mm): " + str(DDepth))                                  
                
                #self.root.ids.res108.text = str(lx + " hi we are bts " + ly)
                
                if float(i_ratio) > 2:        #one-way slab
                    
                    st.write ("Bottom (Tension) Reinforcement:")
                    st.write (str(dia) + " mm dia @ " + str(s_main) + " mm c/c (Main Reinforcement)")
                    st.write (str(dia) + " mm dia @ " + str(sr_dis2) + " mm c/c (Distrubution Reinforcement)")   
                
                    st.write ("Top (Compression) Reinforcement:")
                    st.write (str(dia2) + " mm dia @ " + str(sr_dis_top) + " mm c/c (over the supports)")
                    #self.root.ids.res113.text =  ""
                    
                    st.subheader ("Typical Reinforcement Detailing")
                    st.write ("")
                    st.image("img_1_way_slab_plan.png", width = 400) #caption= "One-way slab plan"
                    st.image("img_1_way_slab_a.png", width = 400) #caption= "One-way slab section A",
                    st.image("img_1_way_slab_b.png", width = 400) #caption= "One-way slab section B", 
                    st.write ("")
                    
                    st.write ("NOTES:")
                    st.write ("1. Cover to reinforcement is 15mm.")
                    st.write ("2. Assume that adequate quality control and safety is attained in casting and placement of reinforcement.")
                    st.write ("3. Kindly refer to the following figures for typical reinforcement detailing in slabs.")

                
                if float(i_ratio) < 2:      #two-way slab
                    st.write ("Bottom (Tension) Reinforcement:")
                    st.write (str(dia) + " mm dia @ " + str(s_main) + " mm c/c (Main Reinforcement)")
                    st.write (str(dia) + " mm dia @ " + str(sr_dis1) + " mm c/c (Distrubution Reinforcement)")        
                
                    if int(y) == 0 or int(y) == 1 or int(y) == 2 or int(y) == 3 or int(y) == 4 or int(y) == 5 or int(y) == 6 or int(y) == 7:
                        st.write ("Top (Compression) Reinforcement:")
                        st.write (str(dia2) + " mm dia @ " + str(s_main_neg) + " mm c/c (Main Reinforcement)")
                        st.write (str(dia2) + " mm dia @ " + str(sr_dis1_neg) + " mm c/c (Distrubution Reinforcement)")
                    
                    if int(y) == 8 or int(y) == 9 or int(y) == 12 or int(y) == 13:    
                        st.write ("Top (Compression) Reinforcement:")
                        st.write (str(dia2) + " mm dia @ " + str(s_main_neg) + " mm c/c (Main Reinforcement)")
                        #self.root.ids.res113.text =  ""
                    
                    if int(y) == 10 or int(y) == 11 or int(y) == 14 or int(y) == 15:    
                        st.write ("Top (Compression) Reinforcement:") 
                        st.write (str(dia2) + " mm dia @ " + str(sr_dis1_neg) + " mm c/c (Distrubution Reinforcement)")
                        #self.root.ids.res113.text =  ""
                        
                    st.subheader ("Typical Reinforcement Detailing")
                    st.write ("")
                    st.image("img_2_way_slab_plan.png", width = 400) #caption= "Two-way slab plan", 
                    st.image("img_2_way_slab_sec_c.png", width = 400) #caption= "Two-way slab section C", 
                    st.image("img_2_way_slab_sec_d.png", width = 400) #caption= "Two-way slab section D", 
                    st.write ("")
                    
                    st.write ("NOTES:")
                    st.write ("1. Cover to reinforcement is 15mm.")
                    st.write ("2. Assume that adequate quality control and safety is attained in casting and placement of reinforcement.")
                    st.write ("3. Kindly refer to the above figures for typical reinforcement detailing in slabs.")

                        
                    
                # print ("---------------------------------------------------------------")
                # print ('\n')
                # print ('\n')
                
                # print ("Both conditions satisfied")
                break
            else:
                print ("else me aaya")
                pt = float (pt) + 0.01
                i = i+1
        
        

            
    
 

        

            
    
        
        
 
