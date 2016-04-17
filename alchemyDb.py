from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///voters.db', echo=True)

Base = declarative_base()

class Voter(Base):
  __tablename__ = 'voters'
  
  id = Column(Integer, primary_key = True)
  electorName = Column(String)
  age = Column(Integer)
  gender = Column(String)
  husbandName = Column(String)
  fatherName = Column(String)
  relationName = Column(String)
  houseName = Column(String)
  houseNum = Column(Integer)
  serialNum = Column(Integer)
  boothNum = Column(Integer, ForeignKey('Booth.boothNum'))
  lacNum = Column(Integer, ForeignKey('Lac.lacNum'))
  psNum = Column(Integer)
  idcardNum = Column(String)
  status = Column(String)

class Blo (Base):
  id = Column(Integer, primary_key = True)
  bloName = Column(String)
  bloJob = Column(String)
  bloAddress = Column(String)
  bloPhone = Column(String)

class Booth(Base):
  boothNum = Column(Integer, primary_key = True)
  boothName = Column(String)

class Lac(Base):
  lacNum = Column(Integer, primary_key = True)
  lacName = Column(String)
  districtNum = Column(Integer, ForeignKey('district.disNum'))
  
class District(Base):
  disNum = Column(Integer, primary_key = True)
  disName = Column(String)
  
  
  def __repr__(self):
    return "<User(name='%s', fullname='%s', password='%s')>" % (
      self.electorName, self.relationName, self.houseName, 
      self.serialNum, self.lacNum, self.psNum, self.idcardNum, self.status)

  
  
  
  
#{'iTotalRecords': 20058, 'ERROR': False, 'errors': [], 'iTotalDisplayRecords': 20058, 'aaData': [['Anju K Mohan', 'Jayakrishna ',
#'Ambadi', '540', '75', '88', '<a title="Roll Search - Detail View"class="thickbox" href="searchDetails.html?height=500&width=800&paramValue=
#0750881488">AFJ0019521</a>', 'Active'], ['Annie Joseph', 'John Joseph', 'Arrakkal ', '820', '75', '72', '<a title="Roll Search - Detail View
#"class="thickbox" href="searchDetails.html?height=500&width=800&paramValue=0750721552">AFJ0298141</a>', 'Active'], ['Anupama Thomas', 'Shaij
#u', 'Pallathatty', '-', '75', '30', '<a title="Roll Search - Detail View"class="thickbox" href="searchDetails.html?height=500&width=800&para
#mValue=0750301894">AFU0116046</a>', 'Deleted(Shifted)'], ['Anie K Joy', 'Jimmi Joseph', 'Njaliyan', '886', '75', '144', '<a title="Roll Sear
#ch - Detail View"class="thickbox" href="searchDetails.html?height=500&width=800&paramValue=0751441598">AFU0155614</a>', 'Active'], ['Anuja T
# M', 'Anoob', 'Thevarmadam', '961', '75', '32', '<a title="Roll Search - Detail View"class="thickbox" href="searchDetails.html?height=500&wi
#dth=800&paramValue=0750321583">AFU0194902</a>', 'Active'], ['Athulya K V', 'Sandeep', 'Kunnil', '-', '75', '18', '<a title="Roll Search - De
#tail View"class="thickbox" href="searchDetails.html?height=500&width=800&paramValue=0750181478">AHQ0349779</a>', 'Active'], ['Arun C Antony'
#, 'C D Antony', 'Chittinappilly', '840', '75', '81', '<a title="Roll Search - Detail View"class="thickbox" href="searchDetails.html?height=5
#00&width=800&paramValue=0750812243">ARA0368720</a>', 'Active'], ['Anumol E K ', 'Sunil M K', 'Machampilly', '172', '75', '61', '<a title="Ro
#ll Search - Detail View"class="thickbox" href="searchDetails.html?height=500&width=800&paramValue=0750611340">AUM0117960</a>', 'Active'], ['
#Annam ', 'Rijo Jose', 'Chakkiath Mooda', '1007', '75', '41', '<a title="Roll Search - Detail View"class="thickbox" href="searchDetails.html?
#height=500&width=800&paramValue=0750411491">AWE0125534</a>', 'Active'], ['Anju Sooraj', 'Sooraj', 'Madassery', '609', '75', '50', '<a title=
#"Roll Search - Detail View"class="thickbox" href="searchDetails.html?height=500&width=800&paramValue=0750501273">AYB0033696</a>', 'Active']]
#}

#
#
#IdCard No	AFJ0019521
#Name of Elector	Anju K Mohan
#Age	29
#Husband's Name	Jayakrishna
#HouseNo./House Name	124 /  Ambadi
#Serial No. in Voters list	540
#Assembly Constituency	075 . ANGAMALY
#Booth	088 . St.Antony's Lower Primary School (West Portion)
#BLO Details	
#Name and Designation	Phone Numbers
#Aliamma K A
#Anganvadi Worker
#ICDS, Angamaly Additional,ICDS, Angamaly Additional
#
#9562223835 (M)
#Status	Active
#Family Members(Electors having same house number in a booth.)
#Name of Elector	Relation Name	House Name	Serial No	LAC No	PS No	IdCard No	Status
#Jaya Prakash	Kunjukrishnan	Ambadi	537	75	88	KL/10/068/054233	Active
#Suganthi	Jaya Prakash	Ambadi	538	75	88	KL/10/068/054490	Active
#Jayakrishna	K Jayaprakash	Ambadi	539	75	88	RZM0247551	Active
#Vijaykrishna J	Jayaprakash K	Ambadi	541	75	88	RZM0247536	Active
#
#
#
#
#<div style="height:750px;">
#   <!-- style="font-family:AnjaliOldLipi,'DejaVu Sans' ;font-style: book" -->
#     	<form id="command" action="/searchDetails.html?height=500&amp;width=800&amp;paramValue=0750881488&amp;random=1460888052823" method="post">
#     	<table width="100%" class="display">
#	        <tbody><tr class="odd"><td width="20%">IdCard No</td><td>AFJ0019521</td></tr> 
#	     	<tr class="even"><td>Name of Elector</td>
#	     	<td>Anju K Mohan <!-- <br/>അഞ്ജു കെ മോഹന്‍  -->	     	
#	     	</td></tr> 
#	     	<tr class="odd"><td>Age</td><td>29 </td></tr> 
#	     	<tr class="even"><td>
#				Husband's Name
#			</td><td>Jayakrishna  
#			<!-- <br/>ജയകൃഷ്ണ ജെ -->
#			</td></tr>
#	     	<tr class="odd"><td>HouseNo./House Name</td>
#	     	<td>124&nbsp;/&nbsp; Ambadi
#	     	<!-- <br/>124&nbsp;/&nbsp; അമ്പാടി -->
#	     	</td></tr>
#	     	<tr class="even"><td>Serial No. in Voters list</td><td>540</td></tr>
#	     	<tr class="odd"><td>Assembly Constituency</td>
#	     	<td>075&nbsp;.&nbsp;ANGAMALY
#	     	<!-- <br/>075&nbsp;.&nbsp;അങ്കമാലി -->
#	     	</td></tr>
#	     	<tr class="even"><td>Booth</td>
#	     	<td>088 . St.Antony's Lower Primary School (West Portion)
#	     	<!-- <br/>088 . സെന്‍റ് ആന്‍റണീസ് ലോവര്‍ പ്രൈമറി സ്ക്കൂള്‍ (പടി.ഭാഗം), ചമ്പന്നൂര്‍-->
#	     	</td></tr>
#	     	<tr class="odd"><td>BLO Details</td><td>
#	     	<table width="100%">
#	     	<tbody><tr><td><b>Name and Designation</b></td><td><b>Phone Numbers</b></td></tr>
#	     	<tr><td>
#	     	Aliamma K A<br>
#	     	Anganvadi Worker<br>
#	     	ICDS, Angamaly Additional,ICDS, Angamaly Additional<br>
#	     	</td>
#	     	<td>
#	     	<br>9562223835<b> (M) </b>
#	     	</td></tr>
#	     	</tbody></table>
#	     	</td>
#	     	</tr>
#	     	<tr class="even"><td>Status</td><td>Active</td></tr>
#	        <tr class="odd"><td colspan="2"> <b>Family Members</b>(Electors having same house number in a booth.)</td></tr>
#		</tbody></table>   	
#		</form>
#		<table id="lst_datatable_e_detail" cellpadding="0" cellspacing="1" border="0" class="display">
#				<thead>
#					<tr>
#						<th style="width:100px">Name of Elector</th>
#						<th style="width:150px">Relation Name</th>
#						<th style="width:150px">House Name</th>
#						<th style="width:40px">Serial No</th>
#						<th style="width:20px">LAC No</th>
#						<th style="width:20px">PS No</th>						
#						<th style="width:150px">IdCard No</th>
#						<th style="width:150px">Status</th>
#					</tr>
#				</thead>
#				<tbody>
#				<tr class="odd">
#				<td>Jaya Prakash</td><td>Kunjukrishnan</td>
#				<td>Ambadi</td>
#				<td>
#				537
#				</td>
#				<td>75</td><td>88</td>
#				<td><a title="Roll Search - Detail View" class="thickbox" href="searchDetails.html?height=500&amp;width=800&amp;paramValue=075088454">KL/10/068/054233</a></td>
#				<td>
#										Active
#				</td>
#				</tr>
#				<tr class="even">
#				<td>Suganthi</td><td>Jaya Prakash</td>
#				<td>Ambadi</td>
#				<td>
#				538
#				</td>
#				<td>75</td><td>88</td>
#				<td><a title="Roll Search - Detail View" class="thickbox" href="searchDetails.html?height=500&amp;width=800&amp;paramValue=075088455">KL/10/068/054490</a></td>
#				<td>
#										Active
#				</td>
#				</tr>
#				<tr class="odd">
#				<td>Jayakrishna </td><td>K Jayaprakash</td>
#				<td>Ambadi</td>
#				<td>
#				539
#				</td>
#				<td>75</td><td>88</td>
#				<td><a title="Roll Search - Detail View" class="thickbox" href="searchDetails.html?height=500&amp;width=800&amp;paramValue=0750881410">RZM0247551</a></td>
#				<td>
#										Active
#				</td>
#				</tr>
#				<tr class="even">
#				<td>Vijaykrishna J</td><td>Jayaprakash K</td>
#				<td>Ambadi</td>
#				<td>
#				541
#				</td>
#				<td>75</td><td>88</td>
#				<td><a title="Roll Search - Detail View" class="thickbox" href="searchDetails.html?height=500&amp;width=800&amp;paramValue=0750881411">RZM0247536</a></td>
#				<td>
#										Active
#				</td>
#				</tr>
#				</tbody>
#			</table>
#</div>







