# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import numpy as np
import pandas as pd
import random
def pageCreation(foto_vis, foto_cb, foto_orig, vis_sim, cb_sim):
    fv = [f for f in foto_vis]
    fc = [f for f in foto_cb]
    
    randList = [0] * len(foto_vis)
    randList.extend([1] * len(foto_cb))
    
    random.shuffle(randList)
    fotoText = ""
    i = 0
    fnum_vis = 0
    fnum_cb = 0
    num_unique = 0
    num_merged = 0
    for f in randList:
        if f ==0:
            fnum_vis = fnum_vis + 1
            fnum = fnum_vis
            foto = fv.pop()
            sim = vis_sim.pop()
            #same foto in both cases
            if foto in foto_cb:
                fotoIncidence = "vis_cb"
                num_merged = num_merged+1
            else:
                fotoIncidence = "vis"
                num_unique = num_unique+1
        else:
            fnum_cb = fnum_cb + 1
            fnum = fnum_cb            
            foto = fc.pop()
            sim = cb_sim.pop()
            #same foto in both cases
            if foto in foto_vis:
                fotoIncidence = "vis_cb"
            else:
                fotoIncidence = "cb"            
            
        fotoText = fotoText + """
            <td valign="top">
                <img class="""+fotoIncidence+""" src="../foto/"""+foto+""".jpg" width="125" /><br/>
                <input class="selector" name="""+"\""+fotoIncidence+"["+str(fnum)+"]\""+"""  type="checkbox" value="1" /> Vybrat <br/>
                <input name="sim["""+str(fnum)+"_"+fotoIncidence+"""]" type="hidden" value="""+str(sim)+""" />
        """    
        i = i+1
        if i % 8 == 0:
           fotoText = fotoText + "<tr>" 
    
    print(num_unique,num_merged)
    
    pageText = """<?php session_start();
            //print_r($_COOKIE);
            //echo session_save_path();
        ?>
        <html>
        <head>
            <title>Line-up evaluation for user """+foto_orig+"""</title>
              <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
              <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
              <script>
              $( function() {
                $( ".selector" ).click(function(){
                    $(this).siblings("img").toggleClass("selectedFoto");
                });
              });


              function scrollTo(id){
                var container = $('body');
                var scrollTo = $(id);
                container.animate({
                    scrollTop: scrollTo.offset().top - container.offset().top + container.scrollTop()
                }); 
              }
              </script>
              <style>
                img {
                    padding:10px;
                }
                .selectedFoto{
                    background-color:red;
                }
              </style>
        </head>
        <body>      
            <h1>Line-up evaluation for user """+foto_orig+"""</h1>
            <h2>Evaluator name:<?php echo $_COOKIE["name"];?>, note: <?php echo $_COOKIE["note"];?></h2>
        <form action="process.php" method="post">
        <input type="hidden" name="lineupID" value=" """+foto_orig+""" " />
        <table>
            <tr><td><img src="../foto/"""+foto_orig+""".jpg" width="125" />
            <tr>
            """+fotoText+"""
        </table>
        <input type="submit" value="Send lineup selection" />
        </form>
        </body>
        </html>
    """
    return pageText

def indexPageCreation(randIDs, users):
    links = ""
    randIDs.sort()
    for p in randIDs:
        uid = users[p]
        links = links + """
            <li><img height="30" src="foto/"""+str(uid)+""".jpg"/> <a href="lineups/lineup"""+str(p)+""".php" >Lineup no. """+str(p)+""" (user id: """+str(uid)+""")</a>
        """
    
    pageText = """<?php
            session_start();
            //ini_set('display_errors', 1);
            //ini_set('display_startup_errors', 1);
            //error_reporting(E_ALL);
            if($_GET["save"]==1){
                setcookie("name",$_POST["evaluator_name"]);
                setcookie("note",$_POST["evaluator_note"]);
                header("Location: http://www.ksi.mff.cuni.cz/~peska/lineup/?msg=savedCredentials");
            }

            
        ?>
        <html>
        <head>
            <title>Line-up evaluation</title>
        </head>
        <body>
            <?php
                $name = $_COOKIE["name"];
                $note = $_COOKIE["note"];
                //print_r($_COOKIE);            
                if($_GET["msg"]=="savedResults"){
                    echo "<h2 style='background-color:green;padding:10px;color:white;'>Last lineup selection saved properly</h2>";
                }
                if($name!="" and $_GET["msg"]=="savedCredentials"){
                    echo "<h2 style='background-color:green;padding:10px;color:white;'>Name and note have been saved</h2>";
                }else if($name=="" and $_GET["msg"]=="savedCredentials"){
                    echo "<h2 style='background-color:red;padding:10px;color:white;'>Error in saving name and note, please try again</h2>";
                }
            
            ?>
            <h1>Evaluator details</h1>
            
            <form action="?save=1" method="post">
            <ul>
                <li>Name: <input type="text" name="evaluator_name" value="<?php echo $name; ?>"/>
                <li>Note: <input type="text" name="evaluator_note" value="<?php echo $note; ?>"/>
            </ul>        
            <input type="submit" value="Save"/>
            <a href="lineups/results.php">Show results for the current evaluator</a>
            </form>
            <h1>Line-up evaluation - list of available experiments</h1>
            <ul>
                """+links+"""
            </ul>

        </body>
        </html>    
    """
    return pageText
if __name__ == "__main__":
    maxM = 4652
    randIDs = [5, 54, 120, 174, 457, 552, 23, 2780, 995, 847, 632, 2754, 1795, 1277, 26, 365, 1500, 2240, 2598, 3996, 3451, 2876, 4041, 1846, 2647, 4313, 3275, 1145, 2746, 3567]

    vv = pd.read_csv("cosineDistance.csv", sep=';', header=None)
    vec_vis = np.asarray(vv)
    
    cb = pd.read_csv("cbDistance.csv", sep=';', header=None)
    vec_cb = np.asarray(cb)
    
    with open("userIDs.csv", "r") as f:
        users = [int(line) for line in f]  
    with open("pageSummary.csv", "w") as pg:   
            pg.write('uid;type;similarity\n')
                
    for uid in randIDs:
        ind_vis = np.argsort(vec_vis[uid,0:maxM])[-21:-1]        
        ind_cb = np.argsort(vec_cb[uid,0:maxM])[-21:-1]
        
        foto_vis = [str(int(users[idU])) for idU in ind_vis]  
        foto_cb = [str(int(users[idU])) for idU in ind_cb] 
        foto_orig = str(int(users[uid]))
        
        with open("pageSummary.csv", "a") as pg:   
            vis_sim = vec_vis[uid,ind_vis].tolist()
            cb_sim = vec_cb[uid,ind_cb].tolist()
            
            pg.write(foto_orig+';orig;\n')
            
            for i in reversed(range(0,len(foto_vis))):
                fv = foto_vis[i]
                sim = vis_sim[i]
                
                pg.write(fv+';vis;'+str(sim)+'\n')
            for i in reversed(range(0,len(foto_cb))):
                fv = foto_cb[i]
                sim = cb_sim[i]
                
                pg.write(fv+';cb;'+str(sim)+'\n')
   
            
    
        pageText = pageCreation(foto_vis, foto_cb, foto_orig, vec_vis[uid,ind_vis].tolist(), vec_cb[uid,ind_cb].tolist())
        with open("lineups/lineup"+str(uid)+".php", "w") as pg:                
            pg.write(pageText)
            
    index = indexPageCreation(randIDs, users)
    with open("index.php", "w") as pg:                
        pg.write(index)
    
