with open('picture_list.txt') as myfile:
    index = 0
    count = len(open('picture_list.txt').readlines())
    #print count
    num = input("input filenums: ")
    every_file_line=count/num
    while count>num*every_file_line:
        every_file_line +=1
    while True:
        index += 1
        try:
            with open('img_'+str(index)+'.txt','w') as f:
            #with open('my-file-%03d.txt' % index, 'w') as f:
                for _ in xrange(every_file_line):
                    f.write(myfile.next())
        except StopIteration:
            break