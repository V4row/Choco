nama =  input('nama kamu siapa? ')
umur = input('umur kamu berapa? ')
kode = input('masukan kode anda ')

punya_duit= True

if nama == 'abel' or 'vebyan' or 'farel':
    print('hallo ' + nama + ' anda diterima')
else:
    print('kamu siapa?')
if umur == 18 or 17 or 19:
    print('umur anda kami kenalabel')
else:
    print('anda tidak kami kenal')
if kode == "222222" :
    import turtle
    turtle.bgcolor('green')
    t = turtle.Turtle()
    for i in range(0,2):
        t.circle(100)
        t.color('green', 'green')
        t.begin_fill()
        t.circle(100)
        
else:
    import turtle
    turtle.bgcolor('red')
    t = turtle.Turtle()
    for i in range(0,5) :
        t.left(120)
        t.forward(100)
        t.left(120)
        t.forward(100)
        t.left(120)
        t.forward(100)
        t.color('red', 'red')
    
    t.hideturtle
    turtle.done


