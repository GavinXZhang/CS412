from django.db import models
from datetime import datetime
# Create your models here.
class Result(models.Model):
    '''
    Store/represent the data from one runner at the Chicago Marathon 2023.
    BIB,First Name,Last Name,CTZ,City,State,Gender,Division,
    Place Overall,Place Gender,Place Division,Start TOD,Finish TOD,Finish,HALF1,HALF2
    '''
    # identification/DOB,DOR
    last_name = models.TextField()
    first_name = models.TextField()
    DOB = models.DateField(null=True, blank=True)  # Change to DateField
    DOR = models.DateField(null=True, blank=True) 
    # Residentials
    SNumber = models.IntegerField()
    SName = models.TextField()
    ApartN = models.TextField()
    ResZip = models.IntegerField()
    # Representation
    Affiliation = models.CharField(max_length=1)
    PNumber = models.TextField()

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField() 
    v23town = models.BooleanField()
    VoterS = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} {self.VoterS}, {self.PNumber}, {self.Affiliation}, {self.DOB},{self.DOR}'
    

def load_data():
    Result.objects.all().delete()
    filename = '/Users/gavinzhang/Desktop/412/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    for line in f:
        fields = [field.strip() for field in line.split(',')]  # strip whitespace from each field
        try:
            dob = datetime.strptime(fields[7], "%Y-%m-%d").date()  # Adjust format if needed
        except ValueError:
            dob = None  # Set to None if DOB format is invalid

        try:
            dor = datetime.strptime(fields[8], "%Y-%m-%d").date()  # Adjust format if needed
        except ValueError:
            dor = None  # Set to None if DOR format is invalid
        # show which value in each field
        try:  
        # create a new instance of Result object with this record from CSV
            result = Result(                    
                    last_name=fields[1],
                    first_name=fields[2],
                    SNumber=int(fields[3]),
                    SName=fields[4],
                    ApartN=fields[5],
                    ResZip=int(fields[6]),
                    DOB=dob,
                    DOR=dor,
                    Affiliation=fields[9].strip(),
                    PNumber= fields[10],
                    v20state=fields[11].strip().upper() == 'TRUE',
                    v21town=fields[12].strip().upper() == 'TRUE',
                    v21primary=fields[13].strip().upper() == 'TRUE',
                    v22general=fields[14].strip().upper() == 'TRUE',
                    v23town=fields[15].strip().upper() == 'TRUE',
                    VoterS=int(fields[16])
                        )
            result.save()
            print(f"Created result: {result}")
        except Exception as e:
            print(f"Skipped: {fields} | Error: {e}")
    print(f'Done. Created {len(Result.objects.all())} Results.')
            