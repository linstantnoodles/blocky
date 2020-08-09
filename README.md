# Blocky

![Time](https://newapproachesme.com/wp-content/uploads/2014/04/3362637206_49f3d68e5c_z.jpg)

Events auditing and scheduling platform. Leverage blocky to gain insight into your life and greater control over your schedule.

## How to Use 

### Configure 

Set your: 

* default wake time
* default sleep time
* working chunks

```
block configure
```

To set up integration with google calendar:

```
block configure gcal
```

### Events

Events are pretty flexible. They can be: 

* Scheduled 
** Overlapping (You can have two scheduled events happening in parallel)
* Unscheduled
* In past, present, or future

While calenders are great at capturing scheduled events, blocky excels at capturing all events as it's goal is to give you the highest possible view of your day, week, month, or any other time range with which you want to use to plan your next events.

List all events today

```
block events -r today
```

List all events for the week

```
block events -r week
```

Starting a timed event between now and now + <block>. This adds a new scheduled event to your log.

```
block events -a "new event" -t 35m
```

You also have the option of persisting it to your calendar with `-p` option.

Just like calendars, you can also _schedule_ an event (future).

```
block events -a "new event" -f <from> <to>
```

If you try to schedule it in the past, you'll get a warning unless you provide the `--past` flag.

To make it recurring, specify `-r` and check off the days you want the event to repeat.

If you're unsure how long something will take, but you want blocky to capture it (when you're done), start a stop watch event: 
```
block events -a "new stop watch event" -sw
```

### Reporting

Show how much time you have remaining in the day in hours, minutes, or seconds

```
block time -r [-m,-s,-h]
```

Show how much time you have in terms of pomodoro cycles (or any custom cycle)

```
block time -r -p or block time -r 50m
```

### Contexts and Tags

Contexts 

When we do things in life, we're often doing them in a particular place - the most common one is work versus home. When you need to organize your room, that happens at home. It's place specific. With covid, work and home is blurred positionally (since everything is done at home), but there are still events (work meetings) that happen specifically in the context of work. 

Often times, that context is time-bound. You may work from home (or not), but for some limited amount of time (9-5). During that period, it doesn't make sense to get available _total_ time, but only the total out of your working context.

Blocky supports the notion of "contexts" for this purpose. All you have to do is switch contexts and all of its api will happen in that context. Contexts must be time bound, so you will get a warning if you try to schedule a meeting past your work time.

```
block configure context "work"
```

Now set your default start and end time and use `block sc work` to switch to the work context and `block current-context` to get the current context. By default, the context is `global`.

Now, listing events will only apply to calendar sources that are tagged with your "work" context. Similarly, adding events will happen directly to your work calendar (if it's set up).


Tags

If contexts are the scopes for blocky, then tags are... well... tags. They're the most flexible form of associating events. Some common tags: 

* cooking
* home-improvement 
* test-prep
* ice-skating-lesson 

This adds power to your reporting which we can provide breakdowns on tags.

To avoid "tag" proliferation, we only allow you to set up tags ahead of time. Think about how you want to tag schedules. 

```
block new 'wow' -t tp,hi
```

Note: as you can see, we can identify tags by their initials.

### Extension / Plugin Infrastructure

At its source, blocky is an events aggregator for your life. You can extend this to do anything: 

* Build events meeting tool. Use blocky as an events backend and layer on top of it users and forms.
* Build complex query layer. Create a tool for analyzing events.

### Blocky Web

You are not limited to the CLI if you create an online account. Don't worry - you have the option of picking a backend (i.e dropbox).

This gives you some additional powers: 

* Hooks to trigger events from anywhere. 
** SMS
** Email
** Web

You can use the underlying blocky infrastructure to log anything from: 

* Time spent on a remote SSH server 
* How long you went running for 
* How long it took to cook something
* How long you spent in a text editor (check out the sublime plugin that integrates with blocky)

Goals:

* Privacy First. You own your data. You choose your backend. Export or purge whenever you want.
* Numerous third party integrations (sublime, vim, chrome). It' all opt-in. Blocky only logs what you want it to log.
* Flexible reporting

