__author__ = 'T Jeremiah - Nov 2015'

import sqlite3 as lite,sys

con = None

try:
    con = lite.connect('pets.db')

    cur = con.cursor()

except lite.Error, e:

    print "Error %s:" % e.args[0]
    sys.exit(1)

personID = None

while personID != -1:

    print "ENTER person's ID Number: (Enter '-1' to Exit)"
    personID = raw_input()

    try:
        personID = int(personID)

    except:
        print "Not valid integer ID, please again"
        continue
    if personID == -1:
        sys.exit(1)

    person_query = "SELECT person.first_name, person.last_name, person.age FROM person WHERE id = ?"

    with con:
        cur.execute(person_query, (personID,))
        data = cur.fetchone()

    if data is not None:
        print "%s %s, %d years old" % (data[0], data[1], data[2])

        cur.execute("DROP TABLE IF EXISTS j;")
        cur.execute("CREATE TABLE j as SELECT pet_id FROM person_pet WHERE person_id = ?", (personID,))
        cur.execute("SELECT pet.name, pet.breed, pet.age, pet.dead FROM pet JOIN j ON j.pet_id = pet.id;")
        pet_data = cur.fetchall()

        for row in pet_data:
            if row[3] == 1:
                tense = ("owned", "was")
            else:
                tense = ("owns", "is")
            print "%s %s %s %s, a %s, that %s %d years old" % (
            data[0], data[1], tense[0], row[0], row[1], tense[1], row[2])
    else:
        print "ERROR. Person can not be located"
