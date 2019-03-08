def ReadRecord(inFilename, outFilename):
    dt = 0.0
    npts = 0

    # Open the input file and catch the error if it can't be read
    inFileID = open(inFilename, 'r')

    # Open output file for writing
    outFileID = open(outFilename, 'w')

    # Flag indicating dt is found and that ground motion
    # values should be read -- ASSUMES dt is on last line
    # of header!!!
    flag = 0

    # Look at each line in the file
    for line in inFileID:
        if line == '\n':
            # Blank line --> do nothing
            continue
        elif flag == 1:
            # Echo ground motion values to output file
            outFileID.write(line)
        else:
            # Search header lines for dt
            words = line.split()
            lengthLine = len(words)

            if lengthLine >= 4:

                if words[0] == 'NPTS=':
                    # old SMD format
                    for word in words:
                        if word != '':
                            # Read in the time step
                            if flag == 1:
                                dt = float(word)
                                break

                            if flag == 2:
                                npts = int(word.strip(','))
                                flag = 0

                            # Find the desired token and set the flag
                            if word == 'DT=' or word == 'dt':
                                flag = 1

                            if word == 'NPTS=':
                                flag = 2


                elif words[-1] == 'DT':
                    # new NGA format
                    count = 0
                    for word in words:
                        if word != '':
                            if count == 0:
                                npts = int(word)
                            elif count == 1:
                                dt = float(word)
                            elif word == 'DT':
                                flag = 1
                                break

                            count += 1

    inFileID.close()
    outFileID.close()

    return dt, npts
