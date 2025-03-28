#print "************************"
print "START OF THE SCRIPT"
print "************************"

# 1. SETTING UP LOOP VARIABLES

Tex_ini = 30
Tex_fin = 233
Tex_step = 1.3

LogN_ini = 12
LogN_fin = 19.2
LogN_step = 0.1

#FreqMin=80000
#FreqMax=400000

inputFile ="/home/gabriel/Downloads/inputmolecules.txt"
outputPath = "/media/sf_11._Shared_VM/1. MADCUBA/SYNTHETIC_SPECTRA"
#outputPath = "/home/gabriel/Downloads/SYNTHETIC_SPECTRA"
cleanThreshold=1e-06

f = open(inputFile,'r')
firstMolecule = 1
for inputlines in f.readlines():
   if len(inputlines.split('/'))<2:
      continue
   if "#" in inputlines:
      continue
   molecule=inputlines.split('/')[0]
   catalog= inputlines.split('/')[1]
   print '%s,%s' %(catalog,molecule)

# 2. OPEN MADCUBA FUNCTIONS
   if firstMolecule:    
      IJ.run("Open Spectra", "select='/home/gabriel/Downloads/ALCHEMI_ACA.data'");
      IJ.run("Select Tab", "nametab=ALCHEMI_ACA.fits");	
      IJ.run("Select Rows", "rows=1#5#");
      IJ.selectWindow("PLOT ALCHEMI_ACA.fits|Orig.");
      firstMolecule= 0
   IJ.run("SLIM Search", " range='selected_data' axislabel='Frequency' axisunit='Hz' molecules='%s       $%s$Any$Any$Any$#' searchtype=new datafile='ALCHEMI_ACA.fits|Orig.' datatype=SPECTRA" % (catalog,molecule));
   IJ.run("SLIM Select Molecule", "molecule='%s' component=1 " % (molecule));
   IJ.run("SLIM Load Transition", "load");
   IJ.run("SLIM Select Rows", "indexrange=0 rows=ALL component=1#");
   IJ.run("SLIM Get Spectrum", "molecules='%s       $%s$Any$Any$Any$#' sort='Intensity' lines='Sel.' type=SIMULATE ");

# 3. SIMULATION 
   currentTex=Tex_ini
   while currentTex<Tex_fin:
      currentLogN=LogN_ini
      while currentLogN<LogN_fin:
         print "%s, %s" % (currentTex,currentLogN)
         print "simulating"
         IJ.run("SLIM SIMULATE", "molecules='%s|1#' logn=%s tex=%s velo=250.0 fwhm=150.0 sourcesize=10.0 fsourcesize=1 intensity=1.0E-4 unit='Jy'" %(molecule,currentLogN,currentTex));
   	 IJ.run("SLIM Get Spectrum", "molecules='%s#' sort='Intensity' lines='Mol.-sel' range=1.0E9 xaxis='Rest_Freq' type=SIMULATE " % (molecule));
# 4. SAVING         
         print "saving"
         IJ.run("SAVE ASCII", "select='%s/file_%s_%s_T%s_N%s'" %(outputPath,catalog,molecule,currentTex,currentLogN));
         print "saved"
#5. CLEANING

         currentLogN+=LogN_step
      currentTex=currentTex*Tex_step
      
print "DONE"
print "************************"
print "START TIME"
print "END TIME"
print "************************"

"""
         if cleanThreshold!=-1:
            print "cleaning"
            f1 = open("'%s/file_%s_%s_T%s_N%s/file_%s_%s_T%s_N%s/$Any'" % (outputPath, catalog, molecule, currentTex, currentLogN,outputPath, catalog, molecule, currentTex, currentLogN), 'r')
            f2 = open('%s/aux.txt' % outputPath, 'w')  # Corregido (sin comillas adicionales)
            for lines in f1.readlines():
               if len(lines.split("\t"))<2:
                  f2.write(lines)
               elif float(lines.split("\t")[1])>cleanThreshold :
                  f2.write("%s\t%10.3e\n" %( lines.split("\t")[0] , float(lines.split("\t")[1]) ) )
            f1.close()
            f2.close()
            os.system('mv %s/aux.txt %s/file_%s_%s_T%s_N%s' %(outputPath,outputPath,catalog,molecule,currentTex,currentLogN) )
            print("cleaned")
            """
