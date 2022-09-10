import pandas as pd

df = pd.read_csv (r'InjuryDataDirty.csv')
print(len(df.Injury.unique()))
rard=df
ps='Position'
p='Player'
i='Injury'
y='Year'
w='Week'
pr='Practice Status'
g='Game Status'

DropWords=['flu','illness','related','covid','illness','virus','personal','persona','infection']

OtherWords=['shortness of breath','other','migraine','reserve','stomach','lung',
            'liver','heat','throat','hernia','kidney','cardiac','sola plexus',
            'pelvis','collarbone','sternoclavicular','sola plexus','glute','sternum',
            'side','appendix','appendectomy','clavicle']

CleanWords=['right','left','upper', 'fracture', 'lower','mid', 'r ', 'rt.', 'l ', 'lt.'
            ,'lf.','l. ', 'r. ', 'strain', 'spasms','injury']

Repeat=['arm','migraines','back','elbow','groin','rib','hip','thigh','quad','shoulder',
        'leg','kidney','ankle','nose','core','bicep','tricep','trap','ear','eye','foot',
        'finger','hand','head','hamstring','knee']


Lower_Leg=['achilles','shin','heel','tibia','fibula','leg','calf']

Abdominal=['core','abdominal','oblique','qblique']
Abdomen=['sola plexus']
Foot=['toe','feet','arch']
Face=['jaw','mouth','tooth','lacerations','laceration','cheek','eye','teeth','chin','nose','ear']
Glutes=['glute','buttocks']
Hand=['thumb','finger']
Thigh=['adductor','quad']
Back=['spine','tailbone','trap','lumbar']
def removedirectionals(x):
    if type(x)!= float:
        x=x.strip()
        x=x.lower()
        for word in CleanWords:
            if word in x:
                x=x.replace(word, ' ')
        return x.strip().capitalize()
    else:
        return x

def drop_noninjuries(x):
    if type(x)!=float:
        x=x.strip()
        x=x.lower()
        for word in DropWords:
            if word in x:
                x='REMOVE'
        return x
    else:
        return x

def checkmult(x):
    if type(x)!=float:
        if len(x.split('/'))>1:
            return x.split('/')
        else:
            return x
    else:
        return x

def combinerepeats(x):
    counter=0
    if type(x)!=float:
        x=x.strip()
        x=x.lower()
        for word in Repeat:
            if word in x:
                x=Repeat[Repeat.index(word)]
            counter+=1
        return x
    else:
        return x

def combinesimilar(x):
    if type(x)!=float:
        x=x.strip()
        x=x.lower()
        for word in Abdominal:
            if word in x:
                x='Abdominal'
        for word in Lower_Leg:
            if word in x:
                x='Lower Leg'
        for word in Face:
            if word in x:
                x='Face'
        for word in Back:
            if word in x:
                x='Back'        
        for word in Thigh:
            if word in x:
                x='Thigh'
        for word in Foot:
            if word in x:
                x='Foot'
        for word in Glutes:
            if word in x:
                x='Glute'
        for word in Hand:
            if word in x:
                x='Hand'
        if 'pectoral' in x:
            x='Chest'
        if x=='stinger':
            x='shoulder'
        return x.strip().capitalize()
        counter=0
    else:
        return x

def turn_into_other(x):
    if type(x)!=float:
        x=x.strip()
        x=x.lower()
        for word in OtherWords:
            if word in x:
                x='Other'
        return x.strip().capitalize()
    else:
        return x
    
def split_multinjs(frame, column):
    x=frame
    col=column
    x[col]=x[col].apply(checkmult)
    return x.explode(col).reset_index(drop=True)

def cleaninjurycolumn(frame,column):
    x=frame
    col=column
    x=split_multinjs(x,col)
    x[col]=x[col].apply(drop_noninjuries)
    x[col]=x[col].apply(removedirectionals)
    x[col]=x[col].apply(combinerepeats)
    x[col]=x[col].apply(combinesimilar)
    x[col]=x[col].apply(turn_into_other)
    return x

## Full Cleaning
df=cleaninjurycolumn(df, 'Injury')
df = df[df['Injury'].notna()]
df = df[df['Player'].notna()]
df = df[df['Position'].notna()]
df=df.drop(df[df['Injury']=='Remove'].index)
df=df.drop(df[df['Game Status']=='Probable'].index)
df=df.drop_duplicates(subset=df.columns.difference(['Week', 'Game Status','Practice Status'])).reset_index(drop=True)
df=df.drop(df[df['Position']=='KR'].index)
df.reset_index(drop=True)
df.Position=df["Position"].replace({'FB':'RB'})
df.Position=df["Position"].replace({'FS':'S'})
df.Position=df["Position"].replace({'SS':'S'})
df.Position=df["Position"].replace({'NT':'DT'})
df.Position=df["Position"].replace({'OLB':'LB'})
df.Position=df["Position"].replace({'MLB':'LB'})

df=df.reset_index(drop=True)
QB=df[df.Position == 'QB']
RB=df[df.Position == 'RB']
WR=df[df.Position == 'WR']
T=df[df.Position == 'T']
G=df[df.Position == 'G']
C=df[df.Position == 'C']
TE=df[df.Position == 'TE']
DE=df[df.Position == 'DE']
DT=df[df.Position == 'DT']
LB=df[df.Position == 'LB']
CB=df[df.Position == 'CB']
P=df[df.Position == 'P']
K=df[df.Position == 'K']
LS=df[df.Position == 'LS']
S=[df.Position == 'S']
Return=pd.concat([df[df.Position == 'PR'],df[df.Position == 'KR']])
Offense=pd.concat([QB,RB,WR,T,G,C,TE])
Skill=pd.concat([QB,RB,WR])
SkillTE=pd.concat([Skill,TE])
Oline=pd.concat([T,G,C])
OlineTE=pd.concat([Oline,TE])
Dline=pd.concat([DT,DE])


df.to_csv('FootballInjuries.csv', encoding='utf-8')


