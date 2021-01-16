from django.http import HttpResponse
from django.shortcuts import render

from pages.forms import PointSubmissionForm
from pages.forms import RewardSubmissionForm
from chores.models import basic_chore
from chores.models import rewards
from pointRequests.models import pointRequest
from pointRequests.models import rewardRequest
from django.shortcuts import redirect

from datetime import date

from people.models import Brandon
from people.models import Jennifer
from people.models import Pandora
from people.models import Violet

from people.models import invalid_passwords

name = ""
task = ""

pswd = "buttFucking"


def home_page(request, *args, **kwargs):
    k = basic_chore.objects.all()

    return render(request, "index.html", {})


def point_submission(request, *args, **kwargs):
    form = PointSubmissionForm(request.POST or None)

    # print( type(form.fields['chore'].widget.choices))

    # form.fields['chore'].widget.choices['butt': 'whole']

    # print( (form.fields['chore'].widget.choices))
    # form.fields['chore'].choices = []
    # 	print(form.fields['chore'].choices)
    choices = []
    for i in basic_chore.objects.all():
        print(i.name.replace("&&", "&nbsp;"))

        form.fields["chore"].widget.choices.append(
            (i.name.replace("&&", "_"), i.name.replace("&&", "_"))
        )

    if form.is_valid():
        form.save()
        form = PointSubmissionForm()
    context = {"form": form}

    return render(request, "point_submission_page.html", context)


def request_submitted(request, *args, **kwargs):
    context = {
        "person": request.POST["name"],
        "chore": request.POST["chore"],
        "date": date.today().strftime("%d-%b-%y"),
    }

    pr = pointRequest(
        name=context["person"],
        chore=context["chore"],
        date=date.today().strftime("%d-%b-%y"),
    )
    pr.save()

    return render(request, "request_submitted.html", context)


def reward_request_submitted(request, *args, **kwargs):
    context = {
        "person": request.POST["name"],
        "chore": request.POST["reward"],
        "date": date.today().strftime("%d-%b-%y"),
    }

    rr = rewardRequest(
        name=context["person"], reward=context["chore"], date=context["date"]
    )
    rr.save()
    return render(request, "reward_request_submitted.html", context)


def pending_requests(request, *args, **kwargs):
    pendingRequests = []
    for i in pointRequest.objects.all():
        pendingRequests.append((i.name, i.chore, i.date))
    context = {"rl": pendingRequests}
    return render(request, "pending_requests.html", context)


def view_reward_requests(request, *args, **kwargs):
    pendingRequestsd = []
    for i in rewardRequest.objects.all():
        pendingRequestsd.append((i.name, i.reward, i.date))
        context = {"rl": pendingRequestsd}
    return render(request, "pending_reward_request.html", context)


def review_task(request, *args, **kwargs):
    print("reviewing for " + request.POST.get("Name"))
    context = {
        "name": request.POST.get("Name"),
        "task": request.POST.get("Task"),
        "date": request.POST.get("Dask"),
    }
    return render(request, "review_task.html", context)


def approve_reward(request, *args, **kwargs):
    context = {
        "name": request.POST.get("Name"),
        "reward": request.POST.get("Reward"),
        "date": request.POST.get("Dask"),
    }
    return render(request, "review_reward.html", context)


def result(request, *args, **kwargs):

    output = ["Name: " + request.POST.get("Name"), "Task: " + request.POST.get("Task")]

    print("task " + request.POST.get("Task"))

    if request.POST.get("shittyPassword") != pswd:
        k = invalid_passwords(
            name=request.POST.get("Name"),
            task=request.POST.get("Task"),
            date=date.today().strftime("%d-%b-%y"),
        )
        k.save()
        return redirect("invalid_password/")

    for i, k in request.POST.items():

        if "approved" in i:
            print("Yay! It has been approved!")
            output.append("Status: Approved")
            context = {"output": output}
            addTaskToDB(
                request.POST.get("Name"),
                request.POST.get("Task"),
                request.POST.get("Unprompted"),
                request.POST.get("Notes"),
                int(request.POST.get("PointAdjustment")),
                request.POST.get("Date"),
            )

        if "denied" in i:
            print("Fuck! It wasn't approved!")
            output.append("Status: Denied")
            context = {"output": output}
            ##addRemarkToDB( request.POST.get('Name'), request.POST.get('Task'), request.POST.get('Notes') )
            print("Action removec")

    return render(request, "result.html", context)


def add_reward_to_db(request, *args, **kwargs):
    results = {
        "name": request.POST.get("Name"),
        "reward": request.POST.get("Reward"),
        "date": request.POST.get("Date"),
    }

    output = ["Name: " + results["name"], "Reward: " + results["reward"]]
    if request.POST.get("shittyPassword") != pswd:
        k = invalid_passwords(
            name=request.POST.get("Name"),
            task=request.POST.get("Task"),
            date=date.today().strftime("%d-%b-%y"),
        )
        k.save()
        return redirect("invalid_password")
    for i, k in request.POST.items():
        if "approved" in i:
            output.append("Status: Approved")
            context = {"output": output}  # REPLACE!
            pointsToTake = 0
            print(i)
            for l in rewards.objects.all():
                print("I'm checking '" + l.name + "' with '" + results["reward"] + "'")
                if l.__eq__(results["reward"]):
                    print("ljlkjlkjlkjlj;" + results["name"])
                    addTaskToDB(
                        results["name"],
                        l.name,
                        False,
                        "",
                        int(l.pointValue * -1),
                        results["date"],
                    )
                    for x in rewardRequest.objects.all():
                        print("Need to remove item from reward reqwest list!")
        if "denied" in i:
            output.append("Status: Denied")
            context = {"output": output}
    return render(request, "result.html", context)


def view_points(request, *args, **kwargs):

    items = getDataFromDatabase(request.POST.get("Name"))

    context = {"name": request.POST.get("Name"), "output": items[0], "points": items[1]}

    return render(request, "view_points.html", context)


def invalid_password_warning(request, *args, **kwargs):
    return render(request, "invalid_password.html", {})


def lapse_of_judgement(request, *args, **kwargs):

    items = []

    for i in invalid_passwords.objects.all():
        items.append((i.date, i.name, i.task))

    context = {"output": items}
    return render(request, "lapse_of_judgement.html", context)


def reward_submission(request, *args, **kwargs):
    form = RewardSubmissionForm(request.POST or None)
    #    reward = []
    for i in rewards.objects.all():
        print(i.name.replace("&&", "_"))
        form.fields["reward"].widget.choices.append(
            (
                i.name.replace("&&", "_"),
                i.name.replace("&&", "_") + ": " + str(i.pointValue) + " points",
            )
        )
    #        form.widget.choices.append((i.name.replace('&&', '_'),i.name, replace('&&', '_')))
    if form.is_valid():
        form.save()
        form = RewardSubmissionForm()
    context = {"form": form}

    return render(request, "reward_submission_page.html", context)


def addTaskToDB(name, task, unprompted, notes, pointAdjustment, dateOfChore):
    print('Oh boy!here i go creating tasks again!')
    k = list(basic_chore.objects.all())
    points = pointAdjustment

    remarks = notes
    newShit = None

    for i in k:

        print( i.name )
        if i.name.replace("&&", "_") == task:
            points = points + i.pointValue

    if unprompted:
        if notes == "":
            remarks = "Unprompted"
        else:
            remarks = "Unprompted/" + notes

        points = points + 5

    print(name)

    if name == "Brandon":
        newShit = Brandon(date=dateOfChore, task=task, remarks=remarks, points=points)

    if name == "Jennifer":
        newShit = Jennifer(date=dateOfChore, task=task, remarks=remarks, points=points)

    if name == "Pandora":
        newShit = Pandora(date=dateOfChore, task=task, remarks=remarks, points=points)

    if name == "Violet":
        newShit = Violet(date=dateOfChore, task=task, remarks=remarks, points=points)

    for i in pointRequest.objects.all():
        if (
            i.name == name
            and i.chore == task.replace("&&", "_")
            and i.date == dateOfChore
        ):
            pointRequest.objects.filter(id=i.id).delete()
            print("Task removed from pending and is now submitted.")
            newShit.save()

            return None
    for i in rewardRequest.objects.all():
        print('============================================')
        print( i )
        print( i.name, name )
        print( i.reward, task )
        print( i.date, dateOfChore)

        #print( i.chore, dateOfChore)
        
        
        if i.name == name and i.reward == task and i.date == dateOfChore:
            print("Herro")
            i.delete()
            newShit.save()
            return 


def addRemarkToDB(name, task):
    if name == "Brandon":
        newShit = Brandon(
            date="Today", task=task, remarks="Nope. Not done right.", points="0"
        )
    if name == "Jennifer":
        newShit = Brandon(
            date="Today", task=task, remarks="Nope. Not done right.", points="0"
        )
    if name == "Pandora":
        newShit = Brandon(
            date="Today", task=task, remarks="Nope. Not done right.", points="0"
        )
    if name == "Violet":
        newShit = Brandon(
            date="Today", task=task, remarks="Nope. Not done right.", points="0"
        )

    newShit.save()


def getDataFromDatabase(name):
    points = 0
    if name == "Brandon":
        li = Brandon.objects.all()
        print(li.count())
        for i in li:
            print(i.date + "  '" + i.task + "'  '" + i.remarks + "'  " + str(i.points))
            points += i.points

        # print( 'returning ' + type(li) + ' items for brandon')
        return (li, points)

    points = 0
    if name == "Jennifer":
        li = Jennifer.objects.all()
        print(li.count())
        for i in li:
            print(i.date + "  '" + i.task + "'  '" + i.remarks + "'  " + str(i.points))
            points += i.points

        # print( 'returning ' + type(li) + ' items for brandon')
        return (li, points)

    points = 0
    if name == "Pandora":
        li = Pandora.objects.all()
        print(li.count())
        for i in li:
            print(i.date + "  '" + i.task + "'  '" + i.remarks + "'  " + str(i.points))
            points += i.points

        # print( 'returning ' + type(li) + ' items for brandon')
        return (li, points)

    points = 0
    if name == "Violet":
        li = Violet.objects.all()
        print(li.count())
        for i in li:
            print(i.date + "  '" + i.task + "'  '" + i.remarks + "'  " + str(i.points))
            points += i.points

        # print( 'returning ' + type(li) + ' items for brandon')
        return (li, points)
